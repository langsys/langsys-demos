"""social-publish: post text, images and videos to YouTube, X and LinkedIn.

    social-publish post --to x,linkedin --text "Hello" --media clip.mp4
    social-publish post --file launch.json --dry-run
    social-publish check
    social-publish auth youtube --client-file client.json --write
    social-publish auth linkedin --write

A post's text and comment can carry {youtube}, {x} or {linkedin}: the link of
what this run posted there. Channels run in that order, so an X post can link
the video uploaded a moment before it.

A post file's results are kept next to it (launch.json -> launch.posted.json),
so running it again posts only to the channels that failed. --force posts
everywhere again.

The same tools are available to an assistant through the MCP server
(python -m social_publisher.mcp_server); see the README.
"""
import argparse
import json
import sys
from pathlib import Path

from . import auth, config, publisher
from .post import CHANNELS, Result

FLAGS = ('text', 'media', 'title', 'comment', 'tags', 'privacy', 'publish_at', 'thumbnail', 'playlist', 'category', 'alt_text')


def main(argv: list[str] | None = None) -> None:
    args = _parser().parse_args(argv)
    env_file = config.load(args.env)
    if args.command == 'post':
        sys.exit(_post(args))
    if args.command == 'check':
        sys.exit(_check(args))
    sys.exit(_auth(args, env_file))


def _parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--env', type=Path, help='the .env file with the tokens (default: ./.env)')

    parser = argparse.ArgumentParser(prog='social-publish', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)

    post = commands.add_parser('post', parents=[common], help='publish a post to one or more channels')
    post.add_argument('--to', help=f"comma-separated channels: {', '.join(CHANNELS)} (default: the file's \"to\")")
    post.add_argument('--file', type=Path, help='a JSON post file; flags given on the command line override it')
    post.add_argument('--text', help='the post text (the description on YouTube)')
    post.add_argument('--text-file', type=Path, help='read the post text from this file')
    post.add_argument('--media', action='append', type=Path, help='an image or video to attach; repeat for several')
    post.add_argument('--alt-text', action='append', help='alt text for the images, in the order of --media; repeat for several')
    post.add_argument('--title', help='the video title on YouTube, the media title on LinkedIn')
    post.add_argument('--comment', help='a first comment (a reply on X)')
    post.add_argument('--tags', help='comma-separated YouTube tags')
    post.add_argument('--privacy', choices=('public', 'unlisted', 'private'), help='YouTube visibility (default: public)')
    post.add_argument('--publish-at', help='schedule the YouTube video, e.g. 2026-11-02T15:00:00-05:00')
    post.add_argument('--thumbnail', type=Path, help='a thumbnail image for the video (YouTube, LinkedIn)')
    post.add_argument('--playlist', help='a YouTube playlist id to add the video to')
    post.add_argument('--category', help='a YouTube category id (default: 28, Science & Technology)')
    post.add_argument('--utm-campaign', help='utm_campaign for the tagged links (default: UTM_CAMPAIGN)')
    post.add_argument('--utm-content', help='utm_content for the tagged links: which video or post this is')
    post.add_argument('--no-utm', action='store_true', help='leave every link as written')
    post.add_argument('--results', type=Path, help='where to keep the results (default: <file>.posted.json next to --file)')
    post.add_argument('--force', action='store_true', help='post again to channels the results say are done')
    post.add_argument('--dry-run', action='store_true', help='check everything and show what would be posted, without posting')
    post.add_argument('--json', action='store_true', help='print the results as JSON')

    check = commands.add_parser('check', parents=[common], help='confirm the tokens work and show who each channel posts as')
    check.add_argument('--to', help='comma-separated channels (default: every channel)')

    sign_in = commands.add_parser('auth', parents=[common], help='sign in once to get the tokens for .env')
    sign_in.add_argument('channel', choices=('youtube', 'linkedin'))
    sign_in.add_argument('--client-file', type=Path, help='youtube: the OAuth client JSON downloaded from Google Cloud')
    sign_in.add_argument('--token-file', type=Path, help='youtube: reuse an existing authorized-user token JSON instead of signing in')
    sign_in.add_argument('--port', type=int, default=8765, help='linkedin: local port for the redirect (default: 8765)')
    sign_in.add_argument('--scopes', default=auth.LINKEDIN_SCOPES, help=f'linkedin: scopes to ask for (default: "{auth.LINKEDIN_SCOPES}")')
    sign_in.add_argument('--write', action='store_true', help='write the tokens into the .env file instead of printing them')
    return parser


def _post(args) -> int:
    try:
        data = json.loads(args.file.read_text(encoding='utf-8')) if args.file else {}
        channels = publisher.channels_from(args.to or data.get('to'))
        results_file = args.results or (args.file.with_name(f'{args.file.stem}.posted.json') if args.file else None)
        base_dir = args.file.resolve().parent if args.file else Path.cwd()
        outcome = publisher.execute(data, channels, base_dir, _overrides(args), results_file, args.force, args.dry_run)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
    if outcome.problems:
        for channel, found in outcome.problems.items():
            for problem in found:
                print(f'{channel}: {problem}', file=sys.stderr)
        print('Nothing was posted.', file=sys.stderr)
        return 2
    if args.dry_run:
        _show_plan(outcome)
        return 0
    _report(outcome.done, outcome.results, args.json)
    return 0 if outcome.ok else 1


def _overrides(args) -> dict:
    overrides = {name: getattr(args, name) for name in FLAGS if getattr(args, name) is not None}
    if args.text_file:
        overrides['text'] = args.text_file.read_text(encoding='utf-8').strip()
    if 'media' in overrides:
        overrides['media'] = [path.resolve() for path in overrides['media']]
    if 'thumbnail' in overrides:
        overrides['thumbnail'] = overrides['thumbnail'].resolve()
    utm = {key: value for key, value in (('campaign', args.utm_campaign), ('content', args.utm_content)) if value}
    if args.no_utm:
        overrides['utm'] = False
    elif utm:
        overrides['utm'] = utm
    return overrides


def _show_plan(outcome: publisher.Outcome) -> None:
    for result in outcome.done:
        print(f'── {result.channel}: already posted, {result.url} (--force to post again)')
    for entry in outcome.plan:
        print(f"── {entry['channel']}")
        if entry.get('title'):
            print(f"   title:   {entry['title']}")
        print('   text:    ' + (entry['text'].replace('\n', '\n            ') or '(none)'))
        alt_texts = entry.get('alt_text', [])
        for index, path in enumerate(entry['media']):
            alt_text = alt_texts[index] if index < len(alt_texts) else ''
            print(f'   media:   {path}' + (f'  (alt: {alt_text})' if alt_text else ''))
        if entry.get('comment'):
            print(f"   comment: {entry['comment']}")
        if entry['channel'] == 'youtube':
            schedule = f" until {entry['publish_at']}" if entry['publish_at'] else ''
            print(f"   privacy: {entry['privacy']}{schedule}")
    print('Dry run: everything checks out; nothing was posted.')


def _report(done: list[Result], results: list[Result], as_json: bool) -> None:
    if as_json:
        print(json.dumps([result.to_dict() for result in done + results], indent=2))
        return
    for result in done:
        print(f'{result.channel:<9} {"done":<7} {result.url}  (posted by an earlier run)')
    for result in results:
        outcome = result.url if result.ok else result.error
        print(f"{result.channel:<9} {'ok' if result.ok else 'FAILED':<7} {outcome}")
        if result.comment_url:
            print(f"{'':<17} comment {result.comment_url}")
        for warning in result.warnings:
            print(f"{'':<17} warning: {warning}")


def _check(args) -> int:
    accounts = publisher.check(publisher.channels_from(args.to) if args.to else list(CHANNELS))
    for account in accounts:
        status = {'ok': 'ok', 'failed': 'FAILED', 'not set up': 'skipped'}[account['status']]
        print(f"{account['channel']:<9} {status:<7} {account.get('account') or account['error']}")
    failed = [account for account in accounts if account['status'] == 'failed' or (args.to and account['status'] != 'ok')]
    return 1 if failed else 0


def _auth(args, env_file: Path) -> int:
    try:
        if args.channel == 'youtube':
            values = auth.youtube(args.client_file, args.token_file)
        else:
            values = auth.linkedin(args.port, args.scopes)
    except Exception as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    if args.write:
        config.upsert(env_file, values)
        print(f"Wrote {', '.join(values)} to {env_file}")
    else:
        print('\n'.join(f'{name}={value}' for name, value in values.items()))
    return 0
