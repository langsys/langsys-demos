"""Building, checking and publishing a post: what the command line and the MCP server share.

A post is described the way a post file is: shared fields at the top level,
each channel's own block ("youtube", "x", "linkedin") over them, and any
overrides (command-line flags, tool arguments) over both.
"""
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .channels import REGISTRY
from .post import CHANNELS, PREVIEW_LINKS, Post, Result


@dataclass
class Outcome:
    problems: dict[str, list[str]] = field(default_factory=dict)
    plan: list[dict] = field(default_factory=list)
    done: list[Result] = field(default_factory=list)
    results: list[Result] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems and all(result.ok for result in self.results)

    def to_dict(self) -> dict:
        return {
            'ok':       self.ok,
            'problems': self.problems,
            'plan':     self.plan,
            'done':     [result.to_dict() for result in self.done],
            'results':  [result.to_dict() for result in self.results],
        }


def channels_from(value: str | list | None) -> list[str]:
    if not value:
        raise ValueError(f"say where to post: any of {', '.join(CHANNELS)}")
    wanted = [name.strip().lower() for name in (value.split(',') if isinstance(value, str) else value)]
    unknown = [name for name in wanted if name not in CHANNELS]
    if unknown:
        raise ValueError(f"unknown channel(s): {', '.join(unknown)}")
    return [channel for channel in CHANNELS if channel in wanted]


def build_posts(data: dict, channels: list[str], base_dir: Path, overrides: dict | None = None) -> dict[str, Post]:
    shared = {key: value for key, value in data.items() if key != 'to' and key not in CHANNELS}
    overrides = overrides or {}
    posts = {}
    for channel in channels:
        fields = {**shared, **(data.get(channel) or {})}
        utm = _merge_utm(fields.get('utm'), overrides['utm']) if 'utm' in overrides else fields.get('utm')
        fields.update({**overrides, 'utm': utm})
        posts[channel] = Post.from_dict(fields, base_dir).tagged(channel)
    return posts


def execute(data: dict, channels: list[str], base_dir: Path, overrides: dict | None = None,
            results_file: Path | None = None, force: bool = False, dry_run: bool = False) -> Outcome:
    """Check every channel, then post to the ones an earlier run with these results has not posted to yet."""
    posts = build_posts(data, channels, base_dir, overrides)
    done = {} if force else load_done(results_file, channels)
    pending = [channel for channel in channels if channel not in done]
    clients, problems = prepare(pending, posts, set(done))
    if problems:
        return Outcome(problems=problems)
    if dry_run:
        return Outcome(plan=plan(pending, posts), done=list(done.values()))
    return Outcome(done=list(done.values()), results=publish(pending, posts, clients, done, results_file))


def prepare(channels: list[str], posts: dict[str, Post], done: set[str]) -> tuple[dict, dict]:
    """Every check runs before anything is posted, so a mistake never leaves a launch half out."""
    clients = {}
    problems = {}
    for position, channel in enumerate(channels):
        post = posts[channel]
        found = [f'uses {{{name}}}, but {name} is not posted before it in this run'
                 for name in post.placeholders() if name not in channels[:position] and name not in done]
        try:
            clients[channel] = REGISTRY[channel].from_env()
            found += clients[channel].validate(post.linked(PREVIEW_LINKS) if not found else post)
        except Exception as error:
            found.append(explain(error))
        if found:
            problems[channel] = found
    return clients, problems


def publish(channels: list[str], posts: dict[str, Post], clients: dict, done: dict[str, Result], results_file: Path | None) -> list[Result]:
    links = {channel: result.url for channel, result in done.items() if result.url}
    results = []
    for channel in channels:
        print(f'{channel}: posting...', file=sys.stderr)
        try:
            result = clients[channel].publish(posts[channel].linked(links))
        except Exception as error:
            result = Result(channel, ok=False, error=explain(error))
        if result.url:
            links[channel] = result.url
        save_result(results_file, result)
        results.append(result)
    return results


def plan(channels: list[str], posts: dict[str, Post]) -> list[dict]:
    """What each channel would get, links tagged; {youtube} and the like stay as written until the run fills them."""
    planned = []
    for channel in channels:
        post = posts[channel]
        entry = {'channel': channel, 'text': post.text, 'media': [str(path) for path in post.media]}
        if post.alt_text:
            entry['alt_text'] = post.alt_text
        if post.comment:
            entry['comment'] = post.comment
        if post.title and channel in ('youtube', 'linkedin'):
            entry['title'] = post.title
        if channel == 'youtube':
            entry.update({'privacy': post.privacy, 'publish_at': post.publish_at, 'tags': post.tags,
                          'thumbnail': str(post.thumbnail) if post.thumbnail else None, 'playlist': post.playlist})
        planned.append(entry)
    return planned


def check(channels: list[str]) -> list[dict]:
    accounts = []
    for channel in channels:
        try:
            accounts.append({'channel': channel, 'status': 'ok', 'account': REGISTRY[channel].from_env().whoami()})
        except Exception as error:
            status = 'not set up' if type(error).__name__ == 'MissingSetting' else 'failed'
            accounts.append({'channel': channel, 'status': status, 'error': explain(error)})
    return accounts


def load_done(results_file: Path | None, channels: list[str]) -> dict[str, Result]:
    """The channels an earlier run with these results already posted to."""
    if not results_file or not results_file.exists():
        return {}
    saved = json.loads(results_file.read_text(encoding='utf-8'))
    return {channel: Result(**saved[channel]) for channel in channels if saved.get(channel, {}).get('ok')}


def save_result(results_file: Path | None, result: Result) -> None:
    if not results_file:
        return
    results_file.parent.mkdir(parents=True, exist_ok=True)
    saved = json.loads(results_file.read_text(encoding='utf-8')) if results_file.exists() else {}
    saved[result.channel] = result.to_dict()
    results_file.write_text(json.dumps(saved, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def explain(error: Exception) -> str:
    if 'invalid_grant' in str(error):
        return ('the YouTube refresh token expired or was revoked; sign in again with '
                '`social-publish auth youtube --client-file <client.json> --write` '
                '(an OAuth app left in "Testing" loses its tokens after 7 days: publish it in the Google Cloud consent screen)')
    return str(error)


def _merge_utm(base: dict | bool | None, override: dict | bool | None) -> dict | bool | None:
    if override is False or override is None:
        return override
    return {**(base if isinstance(base, dict) else {}), **override}
