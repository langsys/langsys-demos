import time

import pytest
import requests
from fakes import FakeResponse, FakeSession

from social_publisher.channels.base import ApiError, call


def testWaitsOutARateLimitThenSucceeds():
    session = FakeSession([
        ('POST', '/tweets', FakeResponse(429, {'title': 'Too Many Requests'}, {'retry-after': '3'})),
        ('POST', '/tweets', FakeResponse(201, {'data': {'id': '1'}})),
    ])
    waits = []

    assert call(session, 'x', 'POST', 'https://api.x.com/2/tweets', sleep=waits.append).status_code == 201
    assert waits == [3.0]


def testALongRateLimitFailsAtOnceAndSaysWhenItResets():
    reset = str(int(time.time()) + 900)
    session = FakeSession([('POST', '/tweets', FakeResponse(429, {}, {'x-rate-limit-reset': reset}))])

    with pytest.raises(ApiError, match='the limit resets at'):
        call(session, 'x', 'POST', 'https://api.x.com/2/tweets', sleep=lambda seconds: None)


def testAServerErrorIsRetriedOnlyWhenTheRequestIsSafeToRepeat():
    session = FakeSession([
        ('GET', '/videos', FakeResponse(503)),
        ('GET', '/videos', FakeResponse(200, {'status': 'AVAILABLE'})),
        ('POST', '/posts', FakeResponse(503)),
    ])
    waits = []

    assert call(session, 'linkedin', 'GET', 'https://api/videos', sleep=waits.append).ok
    assert waits == [2]
    with pytest.raises(ApiError, match='returned 503'):
        call(session, 'linkedin', 'POST', 'https://api/posts', sleep=waits.append)
    assert waits == [2]


def testADroppedConnectionIsRetriedForAnUploadChunk():
    class Flaky(FakeSession):
        def request(self, method, url, **kwargs):
            if not self.calls:
                self.calls.append((method, url, kwargs))
                raise requests.ConnectionError('reset by peer')
            return super().request(method, url, **kwargs)

    session = Flaky([('POST', '/append', FakeResponse(204))])

    assert call(session, 'x', 'POST', 'https://api.x.com/2/media/upload/1/append', sleep=lambda seconds: None, retry=True).ok


def testGivesUpAfterThreeRetries():
    session = FakeSession([('PUT', '/part', FakeResponse(500))] * 4)
    waits = []

    with pytest.raises(ApiError, match='returned 500'):
        call(session, 'linkedin', 'PUT', 'https://upload/part', sleep=waits.append)
    assert waits == [2, 4, 8]
