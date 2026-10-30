import pytest

from social_publisher import utm
from social_publisher.post import Post

SETTINGS = utm.Tagging(('langsys.dev',), 'launch_2026', 'svelte-hero', ('mcp.langsys.dev',))


def testTagsOnlyLinksToTheDomainsAndTheirSubdomains():
    text = 'Start: https://langsys.dev/. Docs (https://docs.langsys.dev/learn?x=1#top), video https://youtu.be/abc'

    assert utm.tag_all(text, 'x', SETTINGS) == (
        'Start: https://langsys.dev/?utm_source=x&utm_campaign=launch_2026&utm_content=svelte-hero. '
        'Docs (https://docs.langsys.dev/learn?x=1&utm_source=x&utm_campaign=launch_2026&utm_content=svelte-hero#top), '
        'video https://youtu.be/abc'
    )


def testLeavesExcludedAndAlreadyTaggedLinksAlone():
    text = 'https://mcp.langsys.dev/mcp and https://langsys.dev/?utm_source=reddit'

    assert utm.tag_all(text, 'linkedin', SETTINGS) == text


def testSettingsComeFromEnvUnlessThePostSetsThem(monkeypatch):
    monkeypatch.setenv('UTM_DOMAINS', 'langsys.dev, example.com')
    monkeypatch.setenv('UTM_CAMPAIGN', 'launch_2026')

    assert utm.tagging(None) == utm.Tagging(('langsys.dev', 'example.com'), 'launch_2026')
    assert utm.tagging({'content': 'demo', 'campaign': 'spring'}).campaign == 'spring'
    assert utm.tagging(False) is None


def testNoTaggingWhenNothingSetsItUp(monkeypatch):
    monkeypatch.delenv('UTM_DOMAINS', raising=False)
    monkeypatch.delenv('UTM_CAMPAIGN', raising=False)

    assert utm.tagging(None) is None
    with pytest.raises(ValueError, match='needs both'):
        utm.tagging({'content': 'demo'})
    with pytest.raises(ValueError, match='unknown utm field'):
        utm.tagging({'medium': 'paid'})


def testEachChannelGetsItsOwnSource(tmp_path):
    post = Post.from_dict({'text': 'https://langsys.dev', 'comment': 'Try https://langsys.dev/start',
                           'utm': {'domains': ['langsys.dev'], 'campaign': 'c'}}, tmp_path)

    assert post.tagged('x').text == 'https://langsys.dev?utm_source=x&utm_campaign=c'
    assert post.tagged('linkedin').comment == 'Try https://langsys.dev/start?utm_source=linkedin&utm_campaign=c'
