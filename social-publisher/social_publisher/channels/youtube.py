"""YouTube, through the Data API v3.

Same steps as langsys-demos/youtube/upload.py: the video goes up private (an
unaudited API project can't set another visibility on upload), is then
switched to the wanted visibility, gets its thumbnail and joins its playlist.
"""
import sys
from datetime import datetime, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from ..config import require
from ..media import inspect, inspect_all, megabytes
from ..post import Post, Result
from .base import step

TOKEN_URI = 'https://oauth2.googleapis.com/token'
SCOPES = ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/youtube.force-ssl']
PRIVACY = ('public', 'unlisted', 'private')
CHUNK = 8 * 1024 * 1024
MAX_THUMBNAIL = 2 * 1024 * 1024
KEPT_STATUS = ('embeddable', 'license', 'publicStatsViewable', 'selfDeclaredMadeForKids')


class YouTube:
    name = 'youtube'

    def __init__(self, service):
        self.service = service

    @classmethod
    def from_env(cls) -> 'YouTube':
        settings = require('YOUTUBE_CLIENT_ID', 'YOUTUBE_CLIENT_SECRET', 'YOUTUBE_REFRESH_TOKEN')
        credentials = Credentials(
            None,
            refresh_token=settings['YOUTUBE_REFRESH_TOKEN'],
            token_uri=TOKEN_URI,
            client_id=settings['YOUTUBE_CLIENT_ID'],
            client_secret=settings['YOUTUBE_CLIENT_SECRET'],
        )
        return cls(build('youtube', 'v3', credentials=credentials, cache_discovery=False))

    def whoami(self) -> str:
        channels = self.service.channels().list(part='snippet', mine=True).execute().get('items', [])
        if not channels:
            raise RuntimeError('signed in, but this login has no YouTube channel; sign in again and pick the channel')
        snippet = channels[0]['snippet']
        return f"{snippet['title']} ({snippet.get('customUrl') or channels[0]['id']})"

    def validate(self, post: Post) -> list[str]:
        problems = []
        media = inspect_all(post.media, problems)
        if len(post.media) != 1 or (media and media[0].kind != 'video'):
            problems.append('needs exactly one video file (an image goes in "thumbnail")')
        if not post.title:
            problems.append('needs a title')
        elif len(post.title) > 100:
            problems.append(f'title is {len(post.title)} characters; the limit is 100')
        if any(character in f'{post.title or ""}{post.text}' for character in '<>'):
            problems.append('YouTube rejects "<" and ">" in the title and description')
        if len(post.text) > 5000:
            problems.append(f'description is {len(post.text)} characters; the limit is 5000')
        if post.privacy not in PRIVACY:
            problems.append(f"privacy must be one of {', '.join(PRIVACY)}")
        if post.publish_at:
            problems.extend(_publish_time_problems(post.publish_at))
        if post.thumbnail:
            thumbnails = inspect_all([post.thumbnail], problems)
            if thumbnails and (thumbnails[0].kind != 'image' or thumbnails[0].size > MAX_THUMBNAIL):
                problems.append(f'thumbnail must be a JPEG or PNG of at most 2 MB ({thumbnails[0].path.name} is {megabytes(thumbnails[0].size)})')
        return problems

    def publish(self, post: Post) -> Result:
        video_id = self._upload(post)
        result = Result(self.name, ok=True, id=video_id, url=f'https://youtu.be/{video_id}')
        if post.privacy != 'private' or post.publish_at:
            step(result, 'visibility', lambda: self._set_status(video_id, post))
        if post.thumbnail:
            step(result, 'thumbnail', lambda: self._set_thumbnail(video_id, post))
        if post.playlist:
            step(result, 'playlist', lambda: self._add_to_playlist(video_id, post.playlist))
        if post.comment:
            step(result, 'comment', lambda: self._comment(video_id, post.comment))
        return result

    def _upload(self, post: Post) -> str:
        video = inspect(post.media[0])
        body = {
            'snippet': {
                'title':       post.title,
                'description': post.text,
                'tags':        post.tags,
                'categoryId':  post.category,
            },
            'status': {
                'privacyStatus':           'private',
                'selfDeclaredMadeForKids': False,
            },
        }
        media = MediaFileUpload(str(video.path), mimetype=video.mime, chunksize=CHUNK, resumable=True)
        request = self.service.videos().insert(part='snippet,status', body=body, media_body=media)
        response = None
        while response is None:
            progress, response = request.next_chunk()
            if progress:
                print(f'  youtube: uploading {int(progress.progress() * 100)}%', end='\r', file=sys.stderr)
        print(' ' * 40, end='\r', file=sys.stderr)
        return response['id']

    def _set_status(self, video_id: str, post: Post) -> None:
        live = self.service.videos().list(part='status', id=video_id).execute()['items'][0]['status']
        status = {key: live[key] for key in KEPT_STATUS if key in live}
        if post.publish_at:
            status.update({'privacyStatus': 'private', 'publishAt': _publish_time(post.publish_at)})
        else:
            status['privacyStatus'] = post.privacy
        self.service.videos().update(part='status', body={'id': video_id, 'status': status}).execute()

    def _set_thumbnail(self, video_id: str, post: Post) -> None:
        thumbnail = inspect(post.thumbnail)
        self.service.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(thumbnail.path), mimetype=thumbnail.mime)).execute()

    def _add_to_playlist(self, video_id: str, playlist_id: str) -> None:
        self.service.playlistItems().insert(part='snippet', body={
            'snippet': {'playlistId': playlist_id, 'resourceId': {'kind': 'youtube#video', 'videoId': video_id}},
        }).execute()

    def _comment(self, video_id: str, text: str) -> None:
        self.service.commentThreads().insert(part='snippet', body={
            'snippet': {'videoId': video_id, 'topLevelComment': {'snippet': {'textOriginal': text}}},
        }).execute()


def _publish_time(value: str) -> str:
    moment = datetime.fromisoformat(value)
    return moment.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _publish_time_problems(value: str) -> list[str]:
    try:
        moment = datetime.fromisoformat(value)
    except ValueError:
        return [f'publish_at {value!r} is not an ISO date-time such as 2026-11-02T15:00:00+00:00']
    if moment.tzinfo is None:
        return [f'publish_at {value!r} needs a timezone, e.g. 2026-11-02T15:00:00-05:00']
    if moment <= datetime.now(timezone.utc):
        return [f'publish_at {value!r} is in the past']
    return []
