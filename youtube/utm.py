"""UTM parameters for every langsys.dev link the campaign publishes, so a
sign-up can be traced back to the platform and the post or video it came from.

    utm_source    where the link sits: youtube, x, linkedin, reddit, ...
    utm_campaign  the campaign, from "utm_campaign" in videos.json
    utm_content   which video or post: the video's file with "/" as "-"

There is no utm_medium: the API works out the kind of placement from the
source (langsys-nova config/attribution.php). Add it by hand only where a
source's usual kind doesn't hold, such as utm_medium=paid on an ad.

The scheme, and which links stay untagged, is in launch/tracking.md.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlencode

CATALOGUE = Path(__file__).parent / 'videos.json'
LANGSYS_LINK = re.compile(r'https://(?:[\w-]+\.)?langsys\.dev[^\s?#`)"\'>]*(?:\?[^\s#`)"\'>]*)?')
ENDPOINT = re.compile(r'https://(?:mcp|api)\.langsys\.dev')
TRY_FREE = 'Try it free'
HOME = 'https://langsys.dev/'


def campaign() -> str:
    return json.loads(CATALOGUE.read_text(encoding='utf-8'))['defaults']['utm_campaign']


def content_of(file: str) -> str:
    return file.replace('/', '-')


def tag(url: str, source: str, content: str, campaign_name: str = None) -> str:
    if 'utm_source=' in url or ENDPOINT.match(url):
        return url
    query = urlencode({
        'utm_source':   source,
        'utm_campaign': campaign_name or campaign(),
        'utm_content':  content,
    })
    return url + ('&' if '?' in url else '?') + query


def tag_all(text: str, source: str, content: str, campaign_name: str = None) -> str:
    """Tags every langsys.dev link in `text` that isn't tagged yet."""
    name = campaign_name or campaign()
    return LANGSYS_LINK.sub(lambda match: tag(match.group(0), source, content, name), text)


def try_free(source: str, content: str, campaign_name: str = None) -> str:
    return f'{TRY_FREE}: {tag(HOME, source, content, campaign_name)}'
