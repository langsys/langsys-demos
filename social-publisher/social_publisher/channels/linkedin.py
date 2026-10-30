"""LinkedIn, through the versioned REST API (/rest/posts, /rest/images, /rest/videos).

Posts as a member (urn:li:person:..., needs w_member_social) or as a company
page (urn:li:organization:..., needs w_organization_social). The commentary
is written in LinkedIn's "little text" format, so its reserved characters are
escaped and each #word becomes a real hashtag. A comment goes on the post.
"""
import re
import time
from urllib.parse import quote

import requests

from ..config import optional, require
from ..media import inspect, inspect_all, megabytes
from ..post import Post, Result
from .base import ApiError, body, call, step

API = 'https://api.linkedin.com/rest'
USERINFO = 'https://api.linkedin.com/v2/userinfo'
DEFAULT_VERSION = '202609'
AUTHOR = re.compile(r'^urn:li:(person|organization):\S+$')
MAX_TEXT = 3000
MAX_IMAGES = 20
MAX_VIDEO = 5 * 1024 * 1024 * 1024
PROCESSING_TIMEOUT = 15 * 60
RESERVED = re.compile(r'([\\|{}@\[\]()<>#*_~])')
HASHTAG = re.compile(r'(?<![\w#])#(\w+)')


class LinkedIn:
    name = 'linkedin'

    def __init__(self, session, author: str, sleep=time.sleep, clock=time.monotonic):
        self.session = session
        self.author = author
        self.sleep = sleep
        self.clock = clock

    @classmethod
    def from_env(cls) -> 'LinkedIn':
        settings = require('LINKEDIN_ACCESS_TOKEN', 'LINKEDIN_AUTHOR')
        session = requests.Session()
        session.headers.update({
            'Authorization':             f"Bearer {settings['LINKEDIN_ACCESS_TOKEN']}",
            'LinkedIn-Version':          optional('LINKEDIN_VERSION', DEFAULT_VERSION),
            'X-Restli-Protocol-Version': '2.0.0',
        })
        return cls(session, settings['LINKEDIN_AUTHOR'])

    def whoami(self) -> str:
        kind, _, identifier = self.author.removeprefix('urn:li:').partition(':')
        if kind == 'organization':
            organization = body(self._call('GET', f'{API}/organizations/{identifier}'))
            return f"{organization.get('localizedName', identifier)} (company page {self.author})"
        user = body(self._call('GET', USERINFO))
        if f"urn:li:person:{user['sub']}" != self.author:
            raise ApiError(f"the token belongs to urn:li:person:{user['sub']}, but LINKEDIN_AUTHOR is {self.author}")
        return f"{user.get('name', user['sub'])} ({self.author})"

    def validate(self, post: Post) -> list[str]:
        problems = []
        if not AUTHOR.match(self.author):
            problems.append('LINKEDIN_AUTHOR must look like urn:li:person:<id> or urn:li:organization:<id>')
        media = inspect_all(post.media, problems)
        if not post.text and not post.media:
            problems.append('needs text or media')
        if len(post.text) > MAX_TEXT:
            problems.append(f'text is {len(post.text)} characters; the limit is {MAX_TEXT}')
        videos = [item for item in media if item.kind == 'video']
        if videos and len(media) > 1:
            problems.append('takes one video, or up to 20 images, not a mix')
        if len(media) > MAX_IMAGES:
            problems.append(f'takes at most {MAX_IMAGES} images; got {len(media)}')
        if videos and videos[0].size > MAX_VIDEO:
            problems.append(f'{videos[0].path.name} is {megabytes(videos[0].size)}; the limit is 5 GB')
        if len(post.alt_text) > len(post.media):
            problems.append(f'has {len(post.alt_text)} alt texts for {len(post.media)} media files')
        if videos and post.alt_text:
            problems.append('alt text goes on images, not on a video')
        if post.thumbnail and not videos:
            problems.append('a thumbnail only goes with a video')
        elif post.thumbnail:
            inspect_all([post.thumbnail], problems)
        return problems

    def publish(self, post: Post) -> Result:
        payload = {
            'author':                    self.author,
            'commentary':                little_text(post.text),
            'visibility':                'PUBLIC',
            'distribution':              {'feedDistribution': 'MAIN_FEED', 'targetEntities': [], 'thirdPartyDistributionChannels': []},
            'lifecycleState':            'PUBLISHED',
            'isReshareDisabledByAuthor': False,
        }
        content = self._content(post)
        if content:
            payload['content'] = content
        response = self._call('POST', f'{API}/posts', json=payload)
        urn = response.headers.get('x-restli-id') or body(response).get('id')
        result = Result(self.name, ok=True, id=urn, url=f'https://www.linkedin.com/feed/update/{urn}/')
        if post.comment:
            step(result, 'comment', lambda: self._comment(urn, post.comment))
        return result

    def _content(self, post: Post) -> dict | None:
        media = [inspect(path) for path in post.media]
        if not media:
            return None
        if media[0].kind == 'video':
            urns = [self._upload_video(media[0], inspect(post.thumbnail) if post.thumbnail else None)]
        else:
            urns = [self._upload_image(item) for item in media]
        alt_texts = post.alt_text + [''] * (len(urns) - len(post.alt_text))
        images = [{'id': urn, **({'altText': alt_text} if alt_text else {})} for urn, alt_text in zip(urns, alt_texts)]
        if len(images) > 1:
            return {'multiImage': {'images': images}}
        return {'media': {**images[0], **({'title': post.title} if post.title else {})}}

    def _upload_image(self, image) -> str:
        started = body(self._call('POST', f'{API}/images', params={'action': 'initializeUpload'}, json={
            'initializeUploadRequest': {'owner': self.author},
        }))['value']
        self._call('PUT', started['uploadUrl'], data=image.path.read_bytes(), headers={'Content-Type': image.mime}, timeout=300)
        self._await_available('images', started['image'])
        return started['image']

    def _upload_video(self, video, thumbnail) -> str:
        started = body(self._call('POST', f'{API}/videos', params={'action': 'initializeUpload'}, json={
            'initializeUploadRequest': {
                'owner':           self.author,
                'fileSizeBytes':   video.size,
                'uploadCaptions':  False,
                'uploadThumbnail': thumbnail is not None,
            },
        }))['value']
        part_ids = []
        with video.path.open('rb') as file:
            for instruction in started['uploadInstructions']:
                file.seek(instruction['firstByte'])
                chunk = file.read(instruction['lastByte'] - instruction['firstByte'] + 1)
                response = self._call('PUT', instruction['uploadUrl'], data=chunk,
                                      headers={'Content-Type': 'application/octet-stream'}, timeout=600)
                part_ids.append(response.headers.get('etag'))
        if thumbnail:
            self._call('PUT', started['thumbnailUploadUrl'], data=thumbnail.path.read_bytes(), headers={'Content-Type': thumbnail.mime})
        self._call('POST', f'{API}/videos', params={'action': 'finalizeUpload'}, json={
            'finalizeUploadRequest': {
                'video':           started['video'],
                'uploadToken':     started.get('uploadToken', ''),
                'uploadedPartIds': part_ids,
            },
        })
        self._await_available('videos', started['video'])
        return started['video']

    def _await_available(self, kind: str, urn: str) -> None:
        deadline = self.clock() + PROCESSING_TIMEOUT
        while True:
            status = body(self._call('GET', f'{API}/{kind}/{quote(urn, safe="")}')).get('status')
            if status == 'AVAILABLE':
                return
            if status == 'PROCESSING_FAILED':
                raise ApiError(f'linkedin could not process {urn}')
            if self.clock() > deadline:
                raise ApiError(f'linkedin still processing {urn} after {PROCESSING_TIMEOUT // 60} minutes')
            self.sleep(5)

    def _comment(self, urn: str, text: str) -> None:
        self._call('POST', f'{API}/socialActions/{quote(urn, safe="")}/comments', json={
            'actor':   self.author,
            'object':  urn,
            'message': {'text': text},
        })

    def _call(self, method: str, url: str, **kwargs):
        return call(self.session, self.name, method, url, sleep=self.sleep, **kwargs)


def little_text(text: str) -> str:
    """Escape LinkedIn's reserved characters, turning each #word into a hashtag."""
    parts = []
    position = 0
    for match in HASHTAG.finditer(text):
        parts.append(RESERVED.sub(r'\\\1', text[position:match.start()]))
        parts.append(f'{{hashtag|\\#|{match.group(1)}}}')
        position = match.end()
    parts.append(RESERVED.sub(r'\\\1', text[position:]))
    return ''.join(parts)
