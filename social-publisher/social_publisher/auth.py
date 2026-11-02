"""One-time sign-ins that produce the tokens the .env file needs.

X needs none: its four tokens come straight from the developer portal.
"""
import json
import secrets
import webbrowser
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from google_auth_oauthlib.flow import InstalledAppFlow

from .channels.youtube import SCOPES as YOUTUBE_SCOPES
from .config import require

LINKEDIN_AUTHORIZE = 'https://www.linkedin.com/oauth/v2/authorization'
LINKEDIN_TOKEN = 'https://www.linkedin.com/oauth/v2/accessToken'
LINKEDIN_USERINFO = 'https://api.linkedin.com/v2/userinfo'
LINKEDIN_SCOPES = 'openid profile w_member_social'


def youtube(client_file: Path | None, token_file: Path | None) -> dict:
    """Sign in through the browser with the OAuth client file, or reuse an existing authorized-user token file."""
    if token_file:
        token = json.loads(token_file.read_text(encoding='utf-8'))
        if not token.get('refresh_token'):
            raise ValueError(f'{token_file} has no refresh_token')
        return {
            'YOUTUBE_CLIENT_ID':     token['client_id'],
            'YOUTUBE_CLIENT_SECRET': token['client_secret'],
            'YOUTUBE_REFRESH_TOKEN': token['refresh_token'],
        }
    if not client_file:
        raise ValueError('pass --client-file (the OAuth client JSON from Google Cloud) or --token-file')
    flow = InstalledAppFlow.from_client_secrets_file(str(client_file), YOUTUBE_SCOPES)
    credentials = flow.run_local_server(port=0, prompt='consent', access_type='offline')
    return {
        'YOUTUBE_CLIENT_ID':     credentials.client_id,
        'YOUTUBE_CLIENT_SECRET': credentials.client_secret,
        'YOUTUBE_REFRESH_TOKEN': credentials.refresh_token,
    }


def linkedin(port: int, scopes: str) -> dict:
    """Sign in through the browser; the app must list http://localhost:<port>/callback as a redirect URL."""
    settings = require('LINKEDIN_CLIENT_ID', 'LINKEDIN_CLIENT_SECRET')
    redirect_uri = f'http://localhost:{port}/callback'
    state = secrets.token_urlsafe(16)
    url = LINKEDIN_AUTHORIZE + '?' + urlencode({
        'response_type': 'code',
        'client_id':     settings['LINKEDIN_CLIENT_ID'],
        'redirect_uri':  redirect_uri,
        'state':         state,
        'scope':         scopes,
    })
    print(f'Opening the browser to sign in to LinkedIn. If it does not open, visit:\n{url}')
    webbrowser.open(url)
    query = _await_callback(port)
    if query.get('state') != state:
        raise ValueError('the sign-in came back with the wrong state; try again')
    if 'error' in query:
        raise ValueError(f"LinkedIn refused: {query['error']} {query.get('error_description', '')}")
    response = requests.post(LINKEDIN_TOKEN, timeout=30, data={
        'grant_type':    'authorization_code',
        'code':          query['code'],
        'redirect_uri':  redirect_uri,
        'client_id':     settings['LINKEDIN_CLIENT_ID'],
        'client_secret': settings['LINKEDIN_CLIENT_SECRET'],
    })
    response.raise_for_status()
    token = response.json()
    expires = date.today() + timedelta(seconds=token['expires_in'])
    print(f'LinkedIn access token expires on {expires.isoformat()}; sign in again before then.')
    values = {'LINKEDIN_ACCESS_TOKEN': token['access_token']}
    if 'openid' in scopes.split():
        user = requests.get(LINKEDIN_USERINFO, headers={'Authorization': f"Bearer {token['access_token']}"}, timeout=30).json()
        values['LINKEDIN_AUTHOR'] = f"urn:li:person:{user['sub']}"
    return values


def _await_callback(port: int) -> dict:
    received = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path != '/callback':
                self.send_response(404)
                self.end_headers()
                return
            received.update({key: values[0] for key, values in parse_qs(parsed.query).items()})
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'Signed in. You can close this tab and go back to the terminal.')

        def log_message(self, *args):
            pass

    server = HTTPServer(('localhost', port), Handler)
    while not received:
        server.handle_request()
    server.server_close()
    return received
