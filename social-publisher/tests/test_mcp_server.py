import json
import sys

import pytest

from social_publisher import mcp_server, publisher
from social_publisher.post import Result


class FakeChannel:
    published = []

    def __init__(self, name):
        self.name = name

    def validate(self, post):
        return [] if post.text else ['needs text or media']

    def publish(self, post):
        FakeChannel.published.append((self.name, post))
        return Result(self.name, ok=True, url=f'https://{self.name}.example/1')

    def whoami(self):
        return f'Langsys on {self.name}'


@pytest.fixture(autouse=True)
def channels(monkeypatch, tmp_path):
    FakeChannel.published = []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('SOCIAL_PUBLISHER_STATE', str(tmp_path / 'state'))
    monkeypatch.setattr(publisher, 'REGISTRY', {name: type(name, (), {'from_env': staticmethod(lambda name=name: FakeChannel(name))}) for name in ('youtube', 'x', 'linkedin')})


def testPreviewShowsEachChannelsPostWithoutPosting(monkeypatch):
    monkeypatch.setenv('UTM_DOMAINS', 'langsys.dev')
    monkeypatch.setenv('UTM_CAMPAIGN', 'launch_2026')
    preview = mcp_server.preview_post(['x', 'linkedin'], text='Try https://langsys.dev', utm_content='hero', linkedin={'comment': 'More soon'})

    assert preview['ok'] and preview['note'] == 'Preview only: nothing was posted.'
    assert FakeChannel.published == []
    planned = {entry['channel']: entry for entry in preview['plan']}
    assert planned['x']['text'] == 'Try https://langsys.dev?utm_source=x&utm_campaign=launch_2026&utm_content=hero'
    assert planned['linkedin']['comment'] == 'More soon'


def testProblemsComeBackInsteadOfPosting():
    outcome = mcp_server.publish_post(['x'])

    assert not outcome['ok']
    assert outcome['problems'] == {'x': ['needs text or media']}
    assert FakeChannel.published == []


def testTheSameCallTwicePostsOnce():
    first = mcp_server.publish_post(['youtube', 'x'], text='Watch {youtube}', youtube={'text': 'Video'})
    second = mcp_server.publish_post(['youtube', 'x'], text='Watch {youtube}', youtube={'text': 'Video'})

    assert first['ok'] and [result['channel'] for result in first['results']] == ['youtube', 'x']
    assert second['results'] == [] and [result['channel'] for result in second['done']] == ['youtube', 'x']
    assert [(name, post.text) for name, post in FakeChannel.published] == [('youtube', 'Video'), ('x', 'Watch https://youtube.example/1')]

    mcp_server.publish_post(['youtube', 'x'], text='Watch {youtube}', youtube={'text': 'Video'}, force=True)
    assert len(FakeChannel.published) == 4


def testStartsFromAPostFileAndKeepsItsResultsNextToIt(tmp_path):
    (tmp_path / 'post.json').write_text(json.dumps({'text': 'From file', 'x': {'text': 'X version'}}))
    outcome = mcp_server.publish_post(['x', 'linkedin'], post_file=str(tmp_path / 'post.json'), comment='Hi')

    assert outcome['ok']
    assert {name: (post.text, post.comment) for name, post in FakeChannel.published} == {'x': ('X version', 'Hi'), 'linkedin': ('From file', 'Hi')}
    assert set(json.loads((tmp_path / 'post.posted.json').read_text())) == {'x', 'linkedin'}


def testCheckAccounts():
    assert mcp_server.check_accounts(['x']) == [{'channel': 'x', 'status': 'ok', 'account': 'Langsys on x'}]


def testServerListsItsThreeTools():
    import asyncio

    tools = asyncio.run(mcp_server.server.list_tools())
    names = {tool.name for tool in tools}

    assert names == {'check_accounts', 'preview_post', 'publish_post'}
    publish = next(tool for tool in tools if tool.name == 'publish_post')
    assert publish.input_schema['required'] == ['to'] if hasattr(publish, 'input_schema') else publish.inputSchema['required'] == ['to']
