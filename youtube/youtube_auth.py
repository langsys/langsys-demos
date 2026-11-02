"""One-time YouTube login for the Langsys channel.

Opens a browser, you sign in and pick the Langsys channel, and the refresh
token is saved next to the OAuth client file. Later scripts load it with
`load_credentials()`. Neither file ever goes in git.
"""

import json
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SECRETS = Path.home() / '.secrets'
CLIENT_FILE = SECRETS / 'youtube-client.json'
TOKEN_FILE = SECRETS / 'youtube-token.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']


def load_credentials() -> Credentials:
    credentials = None
    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if credentials and credentials.valid:
        return credentials
    if credentials and credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
            TOKEN_FILE.write_text(credentials.to_json())
            return credentials
        except Exception:
            pass
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_FILE), SCOPES)
    credentials = flow.run_local_server(port=0, prompt='consent')
    TOKEN_FILE.write_text(credentials.to_json())
    return credentials


if __name__ == '__main__':
    youtube = build('youtube', 'v3', credentials=load_credentials())
    channels = youtube.channels().list(part='snippet', mine=True).execute().get('items', [])
    if not channels:
        sys.exit('Signed in, but this login has no channel. Run again and pick the Langsys channel.')
    snippet = channels[0]['snippet']
    print(json.dumps({'channel': snippet['title'], 'handle': snippet.get('customUrl'), 'id': channels[0]['id']}))
