from fakes import FakeResponse, FakeSession

from social_publisher.channels.x import CHUNK, X, weighted_length
from social_publisher.post import Post


def testPostsTextWithAReply():
    session = FakeSession([
        ('POST', '/2/tweets', FakeResponse(201, {'data': {'id': '1'}})),
        ('POST', '/2/tweets', FakeResponse(201, {'data': {'id': '2'}})),
    ])
    result = X(session).publish(Post(text='Hello', comment='Full video: https://youtu.be/abc'))

    assert result.ok and result.url == 'https://x.com/i/status/1'
    assert result.comment_url == 'https://x.com/i/status/2'
    assert session.calls[0][2]['json'] == {'text': 'Hello'}
    assert session.calls[1][2]['json'] == {'text': 'Full video: https://youtu.be/abc', 'reply': {'in_reply_to_tweet_id': '1'}}


def testUploadsAVideoInChunksAndWaitsForProcessing(files):
    video = files('clip.mp4', CHUNK + 5)
    session = FakeSession([
        ('POST', '/media/upload/initialize', FakeResponse(200, {'data': {'id': 'm1'}})),
        ('POST', '/media/upload/m1/append', FakeResponse(204)),
        ('POST', '/media/upload/m1/append', FakeResponse(204)),
        ('POST', '/media/upload/m1/finalize', FakeResponse(200, {'data': {'processing_info': {'state': 'pending', 'check_after_secs': 1}}})),
        ('GET', '/media/upload', FakeResponse(200, {'data': {'processing_info': {'state': 'succeeded'}}})),
        ('POST', '/2/tweets', FakeResponse(201, {'data': {'id': '9'}})),
    ])
    waits = []
    result = X(session, sleep=waits.append).publish(Post(text='Watch', media=[video]))

    assert result.ok
    assert session.calls[0][2]['json'] == {'media_type': 'video/mp4', 'total_bytes': CHUNK + 5, 'media_category': 'tweet_video'}
    assert [call[2]['data'] for call in session.calls[1:3]] == [{'segment_index': 0}, {'segment_index': 1}]
    assert waits == [1]
    assert session.calls[-1][2]['json'] == {'text': 'Watch', 'media': {'media_ids': ['m1']}}


def testFailedProcessingFailsThePost(files):
    session = FakeSession([
        ('POST', '/initialize', FakeResponse(200, {'data': {'id': 'm1'}})),
        ('POST', '/append', FakeResponse(204)),
        ('POST', '/finalize', FakeResponse(200, {'data': {'processing_info': {'state': 'failed', 'error': {'message': 'bad codec'}}}})),
    ])
    try:
        X(session).publish(Post(media=[files('clip.mp4')]))
    except Exception as error:
        assert 'bad codec' in str(error)
    else:
        raise AssertionError('expected the post to fail')


def testSetsAltTextOnEachImage(files):
    session = FakeSession([
        ('POST', '/initialize', FakeResponse(200, {'data': {'id': 'm1'}})),
        ('POST', '/append', FakeResponse(204)),
        ('POST', '/finalize', FakeResponse(200, {'data': {}})),
        ('POST', '/initialize', FakeResponse(200, {'data': {'id': 'm2'}})),
        ('POST', '/append', FakeResponse(204)),
        ('POST', '/finalize', FakeResponse(200, {'data': {}})),
        ('POST', '/media/metadata', FakeResponse(200, {})),
        ('POST', '/2/tweets', FakeResponse(201, {'data': {'id': '5'}})),
    ])
    X(session).publish(Post(media=[files('a.png'), files('b.png')], alt_text=['The dashboard']))

    assert [call[2].get('json') for call in session.calls if '/metadata' in call[1]] == [{'id': 'm1', 'metadata': {'alt_text': {'text': 'The dashboard'}}}]
    assert session.calls[-1][2]['json']['media'] == {'media_ids': ['m1', 'm2']}


def testValidatesMediaMixAndLength(files):
    channel = X(FakeSession([]))

    assert channel.validate(Post(media=[files('a.mp4'), files('b.png')])) == ['takes up to 4 images, or a single GIF or video, not a mix']
    assert 'takes at most 4 images; got 5' in channel.validate(Post(media=[files(f'{index}.png') for index in range(5)]))
    assert channel.validate(Post(text='a' * 281))[0].startswith('text counts 281 characters')
    assert channel.validate(Post()) == ['needs text or media']
    assert channel.validate(Post(media=[files('a.mp4')], alt_text=['x'])) == ['alt text goes on images and GIFs, not on a video']
    assert channel.validate(Post(media=[files('a.png')], alt_text=['x', 'y'])) == ['has 2 alt texts for 1 media files']


def testCountsLinksAsTwentyThreeCharacters():
    assert weighted_length('see https://example.com/a/very/long/path/that/goes/on') == 4 + 23
    assert weighted_length('日本') == 4
