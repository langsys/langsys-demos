"""Upload the videos listed in videos.json to the Langsys channel.

    python upload.py --day 1          upload every pending video planned for day 1
    python upload.py --limit 5        upload the next 5 pending videos, any day
    python upload.py --dry-run        show what would be uploaded
    python upload.py --replace explainer
                                      delete the uploaded explainer and upload
                                      the current file in its place

Every video goes up private (an unaudited API project can't set another
visibility; switching it to unlisted or public in Studio afterwards works), gets its
thumbnail, and is added to its playlist. Progress is written to uploads.json
after each step, so a run stopped by the daily quota resumes where it left off.
Videos with a "hold" note are skipped until the note is removed, and
"thumbnail": false skips the thumbnail (Shorts, which YouTube covers from a
frame of the video).
"""

import argparse
import json
import sys
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from youtube_auth import load_credentials

HERE = Path(__file__).parent
VIDEOS_DIR = HERE.parent / 'videos'
CATALOGUE = HERE / 'videos.json'
STATE = HERE / 'uploads.json'
DOCS = 'https://docs.langsys.dev'


def _load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding='utf-8'))
    return {'playlists': {}, 'videos': {}}


def _save_state(state: dict) -> None:
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def _is_quota(error: HttpError) -> bool:
    return 'quotaExceeded' in str(error) or 'uploadLimitExceeded' in str(error)


def _description(video: dict, defaults: dict) -> str:
    footer = defaults['footer'].replace('{page}', DOCS + video['page'])
    return f"{video['summary']}\n\n{footer}"


def _playlist_id(youtube, state: dict, key: str, playlists: dict) -> str:
    if key in state['playlists']:
        return state['playlists'][key]
    playlist = playlists[key]
    response = youtube.playlists().insert(part='snippet,status', body={
        'snippet': {'title': playlist['title'], 'description': playlist['description'], 'defaultLanguage': 'en'},
        'status':  {'privacyStatus': 'public'},
    }).execute()
    state['playlists'][key] = response['id']
    _save_state(state)
    print(f"  created playlist '{playlist['title']}'")
    return response['id']


def _upload_video(youtube, video: dict, defaults: dict) -> str:
    body = {
        'snippet': {
            'title':                video['title'],
            'description':          _description(video, defaults),
            'tags':                 defaults['tags'] + video.get('tags', []),
            'categoryId':           defaults['category_id'],
            'defaultLanguage':      defaults['language'],
            'defaultAudioLanguage': defaults['language'],
        },
        'status': {
            'privacyStatus':           defaults['privacy'],
            'selfDeclaredMadeForKids': False,
        },
    }
    media = MediaFileUpload(str(VIDEOS_DIR / f"{video['file']}.mp4"), mimetype='video/mp4', chunksize=8 * 1024 * 1024, resumable=True)
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    response = None
    while response is None:
        progress, response = request.next_chunk()
        if progress:
            print(f'  uploading {int(progress.progress() * 100)}%', end='\r')
    print(f"  uploaded https://youtu.be/{response['id']}   ")
    return response['id']


def _step(state: dict, file: str, name: str, action) -> None:
    record = state['videos'][file]
    if record.get(name):
        return
    try:
        action()
        record[name] = True
        record.pop(f'{name}_error', None)
    except HttpError as error:
        if _is_quota(error):
            raise
        record[f'{name}_error'] = str(error)[:300]
        print(f'  {name} failed: {error}')
    _save_state(state)


def _set_thumbnail(youtube, file: str, video_id: str) -> None:
    thumbnail = VIDEOS_DIR / 'thumbnails' / f'{Path(file).name}.png'
    youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(thumbnail), mimetype='image/png')).execute()


def _retry_thumbnails(state: dict, catalogue: dict) -> None:
    exempt = {video['file'] for video in catalogue['videos'] if video.get('thumbnail') is False}
    missing = [file for file, record in state['videos'].items()
               if record.get('id') and not record.get('thumbnail') and file not in exempt]
    print(f'{len(missing)} thumbnails to set')
    youtube = build('youtube', 'v3', credentials=load_credentials())
    for file in missing:
        record = state['videos'][file]
        record.pop('thumbnail_error', None)
        _step(state, file, 'thumbnail', lambda: _set_thumbnail(youtube, file, record['id']))
        if record.get('thumbnail'):
            print(f'  {file}: thumbnail set')


def _position(state: dict, catalogue: dict, video: dict) -> int:
    """Where the video sits in its playlist: after the videos listed before it
    in the catalogue that are already in, so a replacement keeps its place."""
    earlier = []
    for other in catalogue['videos']:
        if other['file'] == video['file']:
            break
        earlier.append(other)
    return sum(1 for other in earlier
               if other['playlist'] == video['playlist'] and state['videos'].get(other['file'], {}).get('playlist'))


def _forget(youtube, state: dict, file: str) -> None:
    record = state['videos'].pop(file, None)
    if record and record.get('id'):
        youtube.videos().delete(id=record['id']).execute()
        print(f"deleted https://youtu.be/{record['id']} ({file})")
    _save_state(state)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--day', type=int)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--retry-thumbnails', action='store_true')
    parser.add_argument('--replace', nargs='+', metavar='FILE')
    args = parser.parse_args()

    catalogue = json.loads(CATALOGUE.read_text(encoding='utf-8'))
    defaults, state = catalogue['defaults'], _load_state()

    if args.retry_thumbnails:
        _retry_thumbnails(state, catalogue)
        return

    if args.replace:
        unknown = set(args.replace) - {video['file'] for video in catalogue['videos']}
        if unknown:
            sys.exit(f"not in videos.json: {', '.join(sorted(unknown))}")
        if not args.dry_run:
            youtube = build('youtube', 'v3', credentials=load_credentials())
            for file in args.replace:
                _forget(youtube, state, file)

    pending = [video for video in catalogue['videos']
               if not video.get('hold') and not state['videos'].get(video['file'], {}).get('playlist')]
    if args.replace:
        pending = [video for video in catalogue['videos'] if video['file'] in args.replace]
    if args.day:
        pending = [video for video in pending if video['day'] <= args.day]
    if args.limit:
        pending = pending[:args.limit]
    held = [video['file'] for video in catalogue['videos'] if video.get('hold')]

    print(f"{len(pending)} to upload; held: {', '.join(held) or 'none'}")
    if args.dry_run:
        for video in pending:
            print(f"  day {video['day']}  {video['file']}  ->  {video['title']}")
        return

    youtube = build('youtube', 'v3', credentials=load_credentials())
    try:
        for video in pending:
            file = video['file']
            print(f'{file}')
            record = state['videos'].setdefault(file, {})
            if not record.get('id'):
                record['id'] = _upload_video(youtube, video, defaults)
                _save_state(state)
            if video.get('thumbnail') is not False:
                _step(state, file, 'thumbnail', lambda: _set_thumbnail(youtube, file, record['id']))
            _step(state, file, 'playlist', lambda: youtube.playlistItems().insert(part='snippet', body={'snippet': {
                'playlistId': _playlist_id(youtube, state, video['playlist'], catalogue['playlists']),
                'resourceId': {'kind': 'youtube#video', 'videoId': record['id']},
                'position':   _position(state, catalogue, video),
            }}).execute())
    except HttpError as error:
        if not _is_quota(error):
            raise
        _save_state(state)
        sys.exit('Daily YouTube quota used up. Progress saved; run again tomorrow to continue.')


if __name__ == '__main__':
    main()
