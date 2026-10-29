"""Append X and LinkedIn posts for an SDK's calendar days, adapted from the Svelte posts.

    python social_posts.py react

Each port's post is its Svelte original: the framework name swapped, the
port's own clip or cut to upload, and its own YouTube link. A post's text is
often not about any framework; a post that does not name it gains a closing
"Now in React." line, which keeps the repeat from reading as a duplicate.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

import utm

DEMOS = Path(r"C:\laragon\www\langsys-demos")
LABEL = {'react': 'React', 'vue': 'Vue'}
HASHTAG = {'react': '#React', 'vue': '#VueJS'}
FULL_VIDEO = 'Full video in the first comment.'
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def sections(text):
    """Map each post's heading title to its section text."""
    found = {}
    for match in re.finditer(r"^\*\*(?:Short|Video): (.+?)\*\*.*?(?=^## |\Z)", text, re.S | re.M):
        found[match.group(1)] = match.group(0)
    return found


def heading(title):
    title = title.removesuffix(' #Shorts')
    return title.replace('<', '‹').replace('>', '›')


def swap(text, sdk):
    return (text.replace('Svelte devs', f'{LABEL[sdk]} devs').replace('Svelte teams', f'{LABEL[sdk]} teams')
            .replace('#Svelte', HASHTAG[sdk]).replace('Svelte', LABEL[sdk]))


def body_of(section):
    return re.search(r"```\n(.*?)\n```", section, re.S).group(1)


def x_post(section, video, port, sdk, video_id):
    name = Path(video['file']).name
    short = '/social/' in port['file']
    body = swap(body_of(section), sdk)
    if LABEL[sdk] not in body:
        body += f'\n\nNow in {LABEL[sdk]}.'
    if short:
        upload = f"Upload `videos/{sdk}/social/{Path(port['file']).name.removesuffix('-9x16')}-4x5.mp4` (the silent 4:5 cut)."
    else:
        upload = (f"Upload `videos/x/{sdk}/{name}.mp4` (a captioned 30 to 60 second clip of the full video).")
    assert len(body) <= 280, (port['file'], len(body))
    kind = 'Short' if short else 'Video'
    return (f"**{kind}: {heading(port['title'])}** · {len(body)} characters\n\n```\n{body}\n```\n\n"
            f"{upload}\n\nReply:\n\n```\nhttps://youtu.be/{video_id}\n"
            f"{utm.try_free('x', utm.content_of(port['file']))}\n```\n")


def linkedin_post(section, video, port, sdk, video_id):
    name = Path(video['file']).name
    short = '/social/' in port['file']
    body = swap(body_of(section), sdk)
    lines = body.split('\n')
    tags = lines[-1].split()
    if HASHTAG[sdk] not in tags:
        tags = [HASHTAG[sdk]] + tags[:2]
    if LABEL[sdk] not in '\n'.join(lines[:-1]):
        at = lines.index(FULL_VIDEO) if FULL_VIDEO in lines else len(lines) - 1
        lines[at:at] = [f'Now in {LABEL[sdk]}, with the langsys-js-{sdk} SDK.', '']
    lines[-1] = ' '.join(tags)
    body = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines))
    upload = (f"`videos/{sdk}/social/{Path(port['file']).name.removesuffix('-9x16')}-1x1.mp4`" if short
              else f"`videos/x/{sdk}/{name}.mp4`")
    kind = 'Short' if short else 'Video'
    return (f"**{kind}: {heading(port['title'])}**\n\n```\n{body}\n```\n\n"
            f"Upload {upload}.\n\nFirst comment:\n\n```\nhttps://youtu.be/{video_id}\n"
            f"{utm.try_free('linkedin', utm.content_of(port['file']))}\n```\n")


def main():
    sdk = sys.argv[1]
    youtube = DEMOS / 'youtube'
    videos = json.loads((youtube / 'videos.json').read_text(encoding='utf-8'))['videos']
    ids = json.loads((youtube / 'uploads.json').read_text(encoding='utf-8'))['videos']
    by_file = {video['file']: video for video in videos}
    launch = date.fromisoformat(by_file['explainer']['publish'])
    ports = sorted((video for video in videos if video['file'].startswith(f'{sdk}/')), key=lambda v: v['publish'])

    for path, build in ((DEMOS / 'x' / 'posts.md', x_post), (DEMOS / 'linkedin' / 'posts.md', linkedin_post)):
        text = path.read_text(encoding='utf-8')
        assert f'**Video: {LABEL[sdk]} i18n with Langsys' not in text, f'{path} already has {sdk} posts'
        originals = sections(text)
        added = []
        for port in ports:
            leaf = Path(port['file']).name.removeprefix(f'{sdk}-')
            source = f"svelte/social/{leaf}" if '/social/' in port['file'] else f"svelte/{leaf}"
            video = by_file[source]
            section = originals[heading(video['title'])]
            published = date.fromisoformat(port['publish'])
            offset = (published - launch).days
            added.append(f"## Week {offset // 7 + 1}, {DAYS[published.weekday()]} (launch + {offset})\n\n"
                         + build(section, video, port, sdk, ids[port['file']]['id']))
        path.write_text(text.rstrip('\n') + '\n\n' + '\n'.join(added), encoding='utf-8')
        print(f'{path.parent.name}: {len(added)} posts added')


if __name__ == '__main__':
    main()
