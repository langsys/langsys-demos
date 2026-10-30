from fakes import FakeResponse, FakeSession

from social_publisher.channels.linkedin import LinkedIn, little_text
from social_publisher.post import Post

AUTHOR = 'urn:li:organization:42'


def testEscapesReservedCharactersAndKeepsHashtags():
    assert little_text('Ship (now) #React_dev, see_this @you') == 'Ship \\(now\\) {hashtag|\\#|React_dev}, see\\_this \\@you'
    assert little_text('C# is not #1') == 'C\\# is not {hashtag|\\#|1}'


def testPostsTextAndComment():
    session = FakeSession([
        ('POST', '/rest/posts', FakeResponse(201, headers={'x-restli-id': 'urn:li:share:7'})),
        ('POST', '/socialActions/urn%3Ali%3Ashare%3A7/comments', FakeResponse(201, {})),
    ])
    result = LinkedIn(session, AUTHOR).publish(Post(text='Hello #i18n', comment='Video: https://youtu.be/abc'))

    assert result.ok and result.url == 'https://www.linkedin.com/feed/update/urn:li:share:7/'
    payload = session.calls[0][2]['json']
    assert payload['author'] == AUTHOR and payload['commentary'] == 'Hello {hashtag|\\#|i18n}'
    assert 'content' not in payload
    assert session.calls[1][2]['json']['message'] == {'text': 'Video: https://youtu.be/abc'}


def testUploadsAVideoInPartsWithThumbnail(files):
    video = files('clip.mp4', 30)
    thumbnail = files('thumb.png')
    session = FakeSession([
        ('POST', '/rest/videos', FakeResponse(200, {'value': {
            'video':              'urn:li:video:1',
            'uploadToken':        'tok',
            'thumbnailUploadUrl': 'https://upload/thumb',
            'uploadInstructions': [
                {'uploadUrl': 'https://upload/part1', 'firstByte': 0, 'lastByte': 19},
                {'uploadUrl': 'https://upload/part2', 'firstByte': 20, 'lastByte': 29},
            ],
        }})),
        ('PUT', 'part1', FakeResponse(200, headers={'etag': 'e1'})),
        ('PUT', 'part2', FakeResponse(200, headers={'etag': 'e2'})),
        ('PUT', 'thumb', FakeResponse(201)),
        ('POST', '/rest/videos', FakeResponse(200, {})),
        ('GET', '/rest/videos/urn%3Ali%3Avideo%3A1', FakeResponse(200, {'status': 'PROCESSING'})),
        ('GET', '/rest/videos/urn%3Ali%3Avideo%3A1', FakeResponse(200, {'status': 'AVAILABLE'})),
        ('POST', '/rest/posts', FakeResponse(201, headers={'x-restli-id': 'urn:li:share:8'})),
    ])
    waits = []
    result = LinkedIn(session, AUTHOR, sleep=waits.append).publish(Post(text='Watch', media=[video], thumbnail=thumbnail, title='Demo'))

    assert result.ok
    assert [len(call[2]['data']) for call in session.calls[1:3]] == [20, 10]
    assert session.calls[4][2]['params'] == {'action': 'finalizeUpload'}
    assert session.calls[4][2]['json']['finalizeUploadRequest'] == {'video': 'urn:li:video:1', 'uploadToken': 'tok', 'uploadedPartIds': ['e1', 'e2']}
    assert waits == [5]
    assert session.calls[-1][2]['json']['content'] == {'media': {'id': 'urn:li:video:1', 'title': 'Demo'}}


def testSeveralImagesBecomeAMultiImagePost(files):
    script = []
    for index in (1, 2):
        script += [
            ('POST', '/rest/images', FakeResponse(200, {'value': {'uploadUrl': f'https://upload/img{index}', 'image': f'urn:li:image:{index}'}})),
            ('PUT', f'img{index}', FakeResponse(201)),
            ('GET', f'/rest/images/urn%3Ali%3Aimage%3A{index}', FakeResponse(200, {'status': 'AVAILABLE'})),
        ]
    session = FakeSession(script + [('POST', '/rest/posts', FakeResponse(201, headers={'x-restli-id': 'urn:li:share:9'}))])
    LinkedIn(session, AUTHOR).publish(Post(media=[files('a.png'), files('b.jpg')], alt_text=['First screen']))

    assert session.calls[-1][2]['json']['content'] == {'multiImage': {'images': [{'id': 'urn:li:image:1', 'altText': 'First screen'}, {'id': 'urn:li:image:2'}]}}


def testAFailedCommentIsAWarningNotAFailure():
    session = FakeSession([
        ('POST', '/rest/posts', FakeResponse(201, headers={'x-restli-id': 'urn:li:share:7'})),
        ('POST', '/comments', FakeResponse(403, {'message': 'no permission'})),
    ])
    result = LinkedIn(session, AUTHOR).publish(Post(text='Hi', comment='later'))

    assert result.ok
    assert result.warnings[0].startswith('comment: linkedin POST')


def testValidates(files):
    assert LinkedIn(FakeSession([]), 'acme').validate(Post(text='x'))[0].startswith('LINKEDIN_AUTHOR must look like')
    channel = LinkedIn(FakeSession([]), AUTHOR)
    assert channel.validate(Post(media=[files('a.mp4'), files('b.png')])) == ['takes one video, or up to 20 images, not a mix']
    assert channel.validate(Post(text='x', thumbnail=files('t.png'))) == ['a thumbnail only goes with a video']
