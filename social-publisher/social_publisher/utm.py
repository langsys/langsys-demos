"""Campaign tags (UTM) on the links a post shares, so a visit or sign-up can be
traced back to the channel and the post it came from.

    utm_source    the channel the post goes to: youtube, x or linkedin
    utm_campaign  the post's "utm.campaign", or UTM_CAMPAIGN in .env
    utm_content   the post's "utm.content", which video or post this is

Only links to the domains in UTM_DOMAINS (or "utm.domains") and their
subdomains are tagged, never those in UTM_EXCLUDE, and a link that already
carries utm_source is left as it was written. There is no utm_medium: write
it into a link by hand where the source's usual kind doesn't hold.
"""
import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from .config import optional

KEYS = {'domains', 'campaign', 'content', 'exclude'}
LINK = re.compile(r'https?://[^\s<>"\'`]+')
TRAILING = '.,;:!?)]}'


@dataclass(frozen=True)
class Tagging:
    domains: tuple[str, ...]
    campaign: str
    content: str | None = None
    exclude: tuple[str, ...] = ()


def tagging(utm: dict | bool | None) -> Tagging | None:
    """The tagging a post asks for: its own "utm" over the .env defaults, or none when neither sets it up."""
    if utm is False:
        return None
    settings = utm if isinstance(utm, dict) else {}
    unknown = sorted(set(settings) - KEYS)
    if unknown:
        raise ValueError(f"unknown utm field(s): {', '.join(unknown)} (use {', '.join(sorted(KEYS))})")
    domains = _hosts(settings.get('domains') or optional('UTM_DOMAINS', ''))
    campaign = settings.get('campaign') or optional('UTM_CAMPAIGN', '')
    if not settings and not domains and not campaign:
        return None
    if not domains or not campaign:
        raise ValueError('utm tagging needs both the domains to tag (UTM_DOMAINS or utm.domains) and a campaign (UTM_CAMPAIGN or utm.campaign)')
    return Tagging(domains, campaign, settings.get('content'), _hosts(settings.get('exclude') or optional('UTM_EXCLUDE', '')))


def tag_all(text: str, source: str, settings: Tagging) -> str:
    return LINK.sub(lambda match: _tag_match(match.group(0), source, settings), text)


def tag(url: str, source: str, settings: Tagging) -> str:
    parts = urlsplit(url)
    host = (parts.hostname or '').lower()
    if not _within(host, settings.domains) or _within(host, settings.exclude) or 'utm_source' in parse_qs(parts.query):
        return url
    labels = {'utm_source': source, 'utm_campaign': settings.campaign}
    if settings.content:
        labels['utm_content'] = settings.content
    query = f"{parts.query}&{urlencode(labels)}" if parts.query else urlencode(labels)
    return urlunsplit(parts._replace(query=query))


def _tag_match(url: str, source: str, settings: Tagging) -> str:
    link = url.rstrip(TRAILING)
    return tag(link, source, settings) + url[len(link):]


def _hosts(value: str | list) -> tuple[str, ...]:
    names = value.split(',') if isinstance(value, str) else value
    return tuple(name.strip().lower() for name in names if name.strip())


def _within(host: str, domains: tuple[str, ...]) -> bool:
    return any(host == domain or host.endswith(f'.{domain}') for domain in domains)
