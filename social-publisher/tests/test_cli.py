import json

import pytest

from social_publisher import cli, publisher
from social_publisher.post import Post, Result


class FakeChannel:
    published = []

    def __init__(self, name):
        self.name = name

    def validate(self, post):
        return []

    def publish(self, post):
        FakeChannel.published.append((self.name, post))
        urls = {'youtube': 'https://youtu.be/abc', 'x': 'https://x.com/i/status/1', 'linkedin': 'https://www.linkedin.com/feed/update/urn:li:share:1/'}
        return Result(self.name, ok=True, url=urls[self.name])


@pytest.fixture
def channels(monkeypatch, tmp_path):
    FakeChannel.published = []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(publisher, 'REGISTRY', {name: type(name, (), {'from_env': staticmethod(lambda name=name: FakeChannel(name))}) for name in ('youtube', 'x', 'linkedin')})


def testPostFileMergesSharedFieldsChannelOverridesAndFlags(channels, tmp_path, files):
    files('clip.mp4')
    (tmp_path / 'post.json').write_text(json.dumps({
        'to':       ['linkedin', 'youtube', 'x'],
        'text':     'Shared',
        'media':    ['clip.mp4'],
        'youtube':  {'title': 'Demo', 'text': 'Long description'},
        'x':        {'text': 'Short', 'comment': 'Full video: {youtube}'},
        'linkedin': {'comment': 'Video: {youtube}'},
    }))

    with pytest.raises(SystemExit) as exit:
        cli.main(['post', '--file', str(tmp_path / 'post.json'), '--tags', 'a,b'])

    assert exit.value.code == 0
    assert [name for name, _ in FakeChannel.published] == ['youtube', 'x', 'linkedin']
    posts = dict(FakeChannel.published)
    assert posts['youtube'].text == 'Long description' and posts['youtube'].tags == ['a', 'b']
    assert posts['x'].comment == 'Full video: https://youtu.be/abc'
    assert posts['linkedin'].text == 'Shared' and posts['linkedin'].media == [tmp_path / 'clip.mp4']


def testAPlaceholderForAChannelNotInTheRunStopsEverything(channels, capsys):
    with pytest.raises(SystemExit) as exit:
        cli.main(['post', '--to', 'x,linkedin', '--text', 'Watch {youtube}'])

    assert exit.value.code == 2
    assert FakeChannel.published == []
    assert 'uses {youtube}, but youtube is not posted before it' in capsys.readouterr().err


def testDryRunPostsNothing(channels, capsys):
    with pytest.raises(SystemExit) as exit:
        cli.main(['post', '--to', 'x', '--text', 'Hello', '--dry-run'])

    assert exit.value.code == 0
    assert FakeChannel.published == []
    assert 'nothing was posted' in capsys.readouterr().out


def testARerunPostsOnlyWhereTheLastRunFailedAndReusesItsLinks(channels, tmp_path, monkeypatch):
    (tmp_path / 'post.json').write_text(json.dumps({'to': ['youtube', 'x', 'linkedin'], 'text': 'Watch {youtube}', 'youtube': {'text': 'Video'}}))
    (tmp_path / 'post.posted.json').write_text(json.dumps({
        'youtube': Result('youtube', ok=True, url='https://youtu.be/old').to_dict(),
        'x':       Result('x', ok=False, error='boom').to_dict(),
    }))

    with pytest.raises(SystemExit) as exit:
        cli.main(['post', '--file', str(tmp_path / 'post.json')])

    assert exit.value.code == 0
    assert [(name, post.text) for name, post in FakeChannel.published] == [('x', 'Watch https://youtu.be/old'), ('linkedin', 'Watch https://youtu.be/old')]
    saved = json.loads((tmp_path / 'post.posted.json').read_text())
    assert saved['youtube']['url'] == 'https://youtu.be/old' and saved['x']['ok'] and saved['linkedin']['ok']


def testForcePostsEverywhereAgain(channels, tmp_path):
    (tmp_path / 'post.json').write_text(json.dumps({'to': ['x'], 'text': 'Hi'}))
    (tmp_path / 'post.posted.json').write_text(json.dumps({'x': Result('x', ok=True, url='https://x.com/i/status/1').to_dict()}))

    with pytest.raises(SystemExit):
        cli.main(['post', '--file', str(tmp_path / 'post.json'), '--force'])

    assert [name for name, _ in FakeChannel.published] == ['x']


def testUtmFlagsTagLinksPerChannel(channels, monkeypatch):
    monkeypatch.setenv('UTM_DOMAINS', 'langsys.dev')
    monkeypatch.setenv('UTM_CAMPAIGN', 'launch_2026')

    with pytest.raises(SystemExit):
        cli.main(['post', '--to', 'x,linkedin', '--text', 'Try https://langsys.dev', '--utm-content', 'hero'])

    texts = dict((name, post.text) for name, post in FakeChannel.published)
    assert texts['x'] == 'Try https://langsys.dev?utm_source=x&utm_campaign=launch_2026&utm_content=hero'
    assert texts['linkedin'] == 'Try https://langsys.dev?utm_source=linkedin&utm_campaign=launch_2026&utm_content=hero'


def testUnknownFieldsAreRejected(tmp_path):
    with pytest.raises(ValueError, match='unknown post field'):
        Post.from_dict({'txt': 'typo'}, tmp_path)
