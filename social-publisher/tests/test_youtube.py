from unittest.mock import MagicMock

from social_publisher.channels.youtube import YouTube
from social_publisher.post import Post


def _service():
    service = MagicMock()
    service.videos().insert().next_chunk.return_value = (None, {'id': 'vid1'})
    service.videos().list().execute.return_value = {'items': [{'status': {'privacyStatus': 'private', 'embeddable': True, 'uploadStatus': 'uploaded'}}]}
    service.reset_mock()
    return service


def testUploadsPrivateThenSetsVisibilityThumbnailPlaylistAndComment(files):
    service = _service()
    post = Post(text='About it', media=[files('clip.mp4')], title='Demo', privacy='unlisted',
                thumbnail=files('thumb.png'), playlist='PL1', comment='Thanks for watching', tags=['i18n'])
    result = YouTube(service).publish(post)

    assert result.ok and result.url == 'https://youtu.be/vid1' and result.warnings == []
    inserted = service.videos().insert.call_args.kwargs['body']
    assert inserted['status']['privacyStatus'] == 'private'
    assert inserted['snippet'] == {'title': 'Demo', 'description': 'About it', 'tags': ['i18n'], 'categoryId': '28'}
    assert service.videos().update.call_args.kwargs['body'] == {'id': 'vid1', 'status': {'privacyStatus': 'unlisted', 'embeddable': True}}
    assert service.thumbnails().set.call_args.kwargs['videoId'] == 'vid1'
    assert service.playlistItems().insert.call_args.kwargs['body']['snippet']['playlistId'] == 'PL1'
    assert service.commentThreads().insert.call_args.kwargs['body']['snippet']['topLevelComment']['snippet']['textOriginal'] == 'Thanks for watching'


def testSchedulesWithPublishAt(files):
    service = _service()
    YouTube(service).publish(Post(media=[files('clip.mp4')], title='Later', publish_at='2099-01-01T10:00:00-05:00'))

    assert service.videos().update.call_args.kwargs['body']['status']['publishAt'] == '2099-01-01T15:00:00Z'


def testAFailedThumbnailIsAWarning(files):
    service = _service()
    service.thumbnails().set().execute.side_effect = RuntimeError('custom thumbnails need a verified channel')
    result = YouTube(service).publish(Post(media=[files('clip.mp4')], title='T', thumbnail=files('t.png')))

    assert result.ok
    assert result.warnings == ['thumbnail: custom thumbnails need a verified channel']


def testValidates(files):
    channel = YouTube(MagicMock())

    assert channel.validate(Post(media=[files('a.png')], title='T')) == ['needs exactly one video file (an image goes in "thumbnail")']
    assert channel.validate(Post(media=[files('a.mp4')])) == ['needs a title']
    assert channel.validate(Post(media=[files('a.mp4')], title='Use <T>')) == ['YouTube rejects "<" and ">" in the title and description']
    assert channel.validate(Post(media=[files('a.mp4')], title='T', publish_at='2020-01-01T00:00:00+00:00')) == ["publish_at '2020-01-01T00:00:00+00:00' is in the past"]
    assert channel.validate(Post(media=[files('a.mp4')], title='T', thumbnail=files('t.png', 3 * 1024 * 1024)))[0].startswith('thumbnail must be')
