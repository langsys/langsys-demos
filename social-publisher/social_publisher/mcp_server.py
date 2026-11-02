"""MCP server: an assistant checks the accounts, previews a post and publishes it,
with the same checks, campaign tags and results as the command line.

    python -m social_publisher.mcp_server --env C:/path/to/.env

The .env is read again on every call, so new tokens apply without a restart.
A post published without a post file keeps its results under
~/.social-publisher/results (SOCIAL_PUBLISHER_STATE), keyed by its content, so
the same call made twice never posts twice; force=True posts again.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Literal

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from . import config, publisher
from .post import CHANNELS

Channel = Literal['youtube', 'x', 'linkedin']
Privacy = Literal['public', 'unlisted', 'private']

INSTRUCTIONS = """Publishes posts to YouTube, X and LinkedIn.

Always call preview_post first and show the person what each channel will get
(text, media, links with their campaign tags). Call publish_post only after
they confirm: a post goes out publicly at once and cannot be taken back here.

Media paths must be absolute. Each channel can get its own text through the
youtube, x and linkedin arguments. {youtube}, {x} or {linkedin} in a text or
comment becomes the link of what this run posted there; channels run in that
order. If publish_post reports a failed channel, calling it again with the
same arguments posts only to the channels that failed."""

server = MCPServer('social-publisher', instructions=INSTRUCTIONS)
env_file: Path | None = None


@server.tool(annotations=ToolAnnotations(read_only_hint=True, open_world_hint=True))
def check_accounts(channels: list[Channel] | None = None) -> list[dict]:
    """Confirm the tokens in .env work and show which account each channel posts as."""
    config.load(env_file)
    return publisher.check(publisher.channels_from(channels) if channels else list(CHANNELS))


@server.tool(annotations=ToolAnnotations(read_only_hint=True, open_world_hint=True))
def preview_post(
    to: list[Channel],
    text: str = '',
    media: list[str] | None = None,
    title: str | None = None,
    comment: str | None = None,
    alt_text: list[str] | None = None,
    tags: list[str] | None = None,
    privacy: Privacy | None = None,
    publish_at: str | None = None,
    thumbnail: str | None = None,
    playlist: str | None = None,
    utm_content: str | None = None,
    utm_campaign: str | None = None,
    no_utm: bool = False,
    youtube: dict | None = None,
    x: dict | None = None,
    linkedin: dict | None = None,
    post_file: str | None = None,
) -> dict:
    """Check a post for every channel and show exactly what each would get, without posting anything.

    text is the post text (the description on YouTube). media: absolute paths; YouTube takes one
    video, X up to 4 images or one GIF/video, LinkedIn one video or up to 20 images. title is
    required for YouTube. comment is a first comment (a reply on X). alt_text: one per image, in
    media order. tags, privacy (default public), publish_at (ISO with timezone, schedules the
    video), thumbnail and playlist apply to YouTube. youtube, x and linkedin hold that channel's
    own fields over the shared ones, e.g. x={"text": "Short version {youtube}"}. post_file: a JSON
    post file to start from; the other arguments go over its top-level fields.
    """
    return _run(locals(), dry_run=True)


@server.tool(annotations=ToolAnnotations(read_only_hint=False, destructive_hint=False, idempotent_hint=True, open_world_hint=True))
def publish_post(
    to: list[Channel],
    text: str = '',
    media: list[str] | None = None,
    title: str | None = None,
    comment: str | None = None,
    alt_text: list[str] | None = None,
    tags: list[str] | None = None,
    privacy: Privacy | None = None,
    publish_at: str | None = None,
    thumbnail: str | None = None,
    playlist: str | None = None,
    utm_content: str | None = None,
    utm_campaign: str | None = None,
    no_utm: bool = False,
    youtube: dict | None = None,
    x: dict | None = None,
    linkedin: dict | None = None,
    post_file: str | None = None,
    force: bool = False,
) -> dict:
    """Publish a post to the given channels. Run preview_post first and get the person's go-ahead.

    Takes the same arguments as preview_post. Every channel is checked before anything is posted.
    Calling it again with the same arguments posts only to the channels that failed, reusing the
    links already posted; force=True posts to every channel again.
    """
    return _run(locals(), dry_run=False)


def _run(arguments: dict, dry_run: bool) -> dict:
    config.load(env_file)
    try:
        data, base_dir, results_file = _post(arguments)
        channels = publisher.channels_from(arguments['to'])
        if results_file is None:
            results_file = _state_file(data, channels)
        outcome = publisher.execute(data, channels, base_dir, None, results_file, arguments.get('force', False), dry_run)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        return {'ok': False, 'problems': {'post': [str(error)]}}
    summary = outcome.to_dict()
    if outcome.problems:
        summary['note'] = 'Nothing was posted.'
    elif dry_run:
        summary['note'] = 'Preview only: nothing was posted.'
    return summary


def _post(arguments: dict) -> tuple[dict, Path, Path | None]:
    """The post as a post file would describe it, the folder relative paths start from, and its results file."""
    post_file = Path(arguments['post_file']).expanduser() if arguments.get('post_file') else None
    data = json.loads(post_file.read_text(encoding='utf-8')) if post_file else {}
    fields = ('text', 'media', 'title', 'comment', 'alt_text', 'tags', 'privacy', 'publish_at', 'thumbnail', 'playlist')
    data.update({name: arguments[name] for name in fields if arguments.get(name)})
    for channel in CHANNELS:
        if arguments.get(channel):
            data[channel] = {**(data.get(channel) or {}), **arguments[channel]}
    utm = {key: arguments[f'utm_{key}'] for key in ('content', 'campaign') if arguments.get(f'utm_{key}')}
    if arguments.get('no_utm'):
        data['utm'] = False
    elif utm:
        data['utm'] = {**(data['utm'] if isinstance(data.get('utm'), dict) else {}), **utm}
    if post_file:
        return data, post_file.resolve().parent, post_file.with_name(f'{post_file.stem}.posted.json')
    return data, Path.cwd(), None


def _state_file(data: dict, channels: list[str]) -> Path:
    state = Path(os.getenv('SOCIAL_PUBLISHER_STATE') or Path.home() / '.social-publisher' / 'results')
    key = hashlib.sha256(json.dumps({'to': channels, **data}, sort_keys=True, default=str).encode()).hexdigest()[:16]
    return state / f'{key}.json'


def main() -> None:
    global env_file
    parser = argparse.ArgumentParser(prog='social-publisher-mcp', description='Run the social-publisher MCP server over stdio.')
    parser.add_argument('--env', type=Path, default=os.getenv('SOCIAL_PUBLISHER_ENV'), help='the .env file with the tokens')
    env_file = parser.parse_args().env
    server.run('stdio')


if __name__ == '__main__':
    main()
