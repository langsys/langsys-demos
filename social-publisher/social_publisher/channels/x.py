"""X, through the API v2 with OAuth 1.0a user tokens (they never expire).

Media goes up in chunks through /2/media/upload (initialize, append,
finalize, then status polling while X processes a video), and the post
through /2/tweets. A comment is posted as a reply to the post.
"""
import re
import time

from requests_oauthlib import OAuth1Session

from ..config import optional, require
from ..media import inspect, inspect_all, megabytes
from ..post import Post, Result
from .base import ApiError, body, call, step

API = 'https://api.x.com/2'
CHUNK = 4 * 1024 * 1024
CATEGORY = {'image': 'tweet_image', 'gif': 'tweet_gif', 'video': 'tweet_video'}
MAX_SIZE = {'image': 5 * 1024 * 1024, 'gif': 15 * 1024 * 1024, 'video': 512 * 1024 * 1024}
MAX_ALT = 1000
URL = re.compile(r'https?://\S+')
URL_LENGTH = 23
SINGLE_WEIGHT = ((0x0000, 0x10FF), (0x2000, 0x200D), (0x2010, 0x201F), (0x2032, 0x2037))


class X:
    name = 'x'

    def __init__(self, session, max_chars: int = 280, sleep=time.sleep):
        self.session = session
        self.max_chars = max_chars
        self.sleep = sleep

    @classmethod
    def from_env(cls) -> 'X':
        settings = require('X_API_KEY', 'X_API_SECRET', 'X_ACCESS_TOKEN', 'X_ACCESS_TOKEN_SECRET')
        session = OAuth1Session(
            settings['X_API_KEY'],
            client_secret=settings['X_API_SECRET'],
            resource_owner_key=settings['X_ACCESS_TOKEN'],
            resource_owner_secret=settings['X_ACCESS_TOKEN_SECRET'],
        )
        return cls(session, int(optional('X_MAX_CHARS', '280')))

    def whoami(self) -> str:
        user = body(self._call('GET', '/users/me'))['data']
        return f"{user['name']} (@{user['username']})"

    def validate(self, post: Post) -> list[str]:
        problems = []
        media = inspect_all(post.media, problems)
        if not post.text and not post.media:
            problems.append('needs text or media')
        kinds = [item.kind for item in media]
        if any(kind != 'image' for kind in kinds) and len(kinds) > 1:
            problems.append('takes up to 4 images, or a single GIF or video, not a mix')
        if len(kinds) > 4:
            problems.append(f'takes at most 4 images; got {len(kinds)}')
        for item in media:
            if item.size > MAX_SIZE[item.kind]:
                problems.append(f'{item.path.name} is {megabytes(item.size)}; the limit for a {item.kind} is {megabytes(MAX_SIZE[item.kind])}')
        if len(post.alt_text) > len(post.media):
            problems.append(f'has {len(post.alt_text)} alt texts for {len(post.media)} media files')
        if any(item.kind == 'video' for item in media) and post.alt_text:
            problems.append('alt text goes on images and GIFs, not on a video')
        problems.extend(f'alt text {index} is {len(text)} characters; the limit is {MAX_ALT}'
                        for index, text in enumerate(post.alt_text, 1) if len(text) > MAX_ALT)
        for label, text in (('text', post.text), ('comment', post.comment or '')):
            if weighted_length(text) > self.max_chars:
                problems.append(f'{label} counts {weighted_length(text)} characters; the limit is {self.max_chars} (set X_MAX_CHARS for X Premium)')
        return problems

    def publish(self, post: Post) -> Result:
        media_ids = [self._upload(inspect(path)) for path in post.media]
        for media_id, alt_text in zip(media_ids, post.alt_text):
            if alt_text:
                self._call('POST', '/media/metadata', json={'id': media_id, 'metadata': {'alt_text': {'text': alt_text}}})
        payload = {'text': post.text}
        if media_ids:
            payload['media'] = {'media_ids': media_ids}
        post_id = body(self._call('POST', '/tweets', json=payload))['data']['id']
        result = Result(self.name, ok=True, id=post_id, url=f'https://x.com/i/status/{post_id}')
        if post.comment:
            step(result, 'comment', lambda: self._reply(result, post.comment))
        return result

    def _reply(self, result: Result, text: str) -> None:
        reply = {'text': text, 'reply': {'in_reply_to_tweet_id': result.id}}
        reply_id = body(self._call('POST', '/tweets', json=reply))['data']['id']
        result.comment_url = f'https://x.com/i/status/{reply_id}'

    def _upload(self, media) -> str:
        started = body(self._call('POST', '/media/upload/initialize', json={
            'media_type':     media.mime,
            'total_bytes':    media.size,
            'media_category': CATEGORY[media.kind],
        }))
        media_id = started['data']['id']
        with media.path.open('rb') as file:
            for index, chunk in enumerate(iter(lambda: file.read(CHUNK), b'')):
                self._call('POST', f'/media/upload/{media_id}/append', data={'segment_index': index},
                           files={'media': ('chunk', chunk, 'application/octet-stream')}, timeout=300, retry=True)
        finished = body(self._call('POST', f'/media/upload/{media_id}/finalize'))
        self._await_processing(media_id, finished.get('data', {}).get('processing_info'))
        return media_id

    def _await_processing(self, media_id: str, info: dict | None) -> None:
        while info and info.get('state') in ('pending', 'in_progress'):
            self.sleep(info.get('check_after_secs', 2))
            status = body(self._call('GET', '/media/upload', params={'media_id': media_id, 'command': 'STATUS'}))
            info = status.get('data', {}).get('processing_info')
        if info and info.get('state') == 'failed':
            raise ApiError(f"x could not process the media: {info.get('error', info)}")

    def _call(self, method: str, path: str, **kwargs):
        return call(self.session, self.name, method, f'{API}{path}', sleep=self.sleep, **kwargs)


def weighted_length(text: str) -> int:
    """Characters as X counts them: a link is 23, most CJK characters and emoji are 2."""
    length = 0
    position = 0
    for match in URL.finditer(text):
        length += _weigh(text[position:match.start()]) + URL_LENGTH
        position = match.end()
    return length + _weigh(text[position:])


def _weigh(text: str) -> int:
    return sum(1 if any(low <= ord(character) <= high for low, high in SINGLE_WEIGHT) else 2 for character in text)
