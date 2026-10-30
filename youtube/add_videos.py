"""Add the React and Vue ports to videos.json and the 17 localization files.

    python add_videos.py

Each port copies its Svelte entry: the framework name swapped where the
title names it, "(React)" appended where it does not (so the channel never
shows two identical titles), the SDK's own docs page, and SDK tags. The same
substitutions apply to every localization, since a framework name is not
translated. Dates continue the calendar's rhythm after the last Svelte-era
video: how-to videos Monday, Wednesday and Friday, Shorts Tuesday and Thursday.
"""
import json
from datetime import date, timedelta
from pathlib import Path

YOUTUBE = Path(r"C:\laragon\www\langsys-demos\youtube")
CATALOGUE = YOUTUBE / 'videos.json'

SDKS = {
    'react': dict(label='React', day=8, tags={
        'svelte i18n': 'react i18n', 'sveltekit i18n': 'next.js i18n', 'svelte': 'react',
        'sveltekit': 'nextjs', 'svelte translation': 'react translation', 'svelte 5': 'react 19',
        'svelte tutorial': 'react tutorial', 'svelte plurals': 'react plurals', 'Svelte': 'React'}),
    'vue': dict(label='Vue', day=9, tags={
        'svelte i18n': 'vue i18n', 'sveltekit i18n': 'nuxt i18n', 'svelte': 'vue',
        'sveltekit': 'nuxt', 'svelte translation': 'vue translation', 'svelte 5': 'vue 3',
        'svelte tutorial': 'vue tutorial', 'svelte plurals': 'vue plurals', 'Svelte': 'Vue'}),
}

LONG = ['hero', 't-string', 'phrase-tag', 'translate-tag', 'donttranslate', 'content-blocks',
        'categories', 'icu-gender', 'attributes', 'formatting']
SHORTS = ['phrase', 'icu-plurals', 'bold-moves', 'content-blocks', 'brand-names', 'icu-gender',
          'two-meanings', 'alt-text', 'local-formats']


def retitle(title, label):
    if 'Svelte' in title:
        return title.replace('Svelte', label)
    if title.endswith(' #Shorts'):
        return title[:-len(' #Shorts')] + f' ({label}) #Shorts'
    return f'{title} ({label})'


def repage(page, sdk):
    if not page.startswith('/learn/sdk/svelte'):
        return page
    return f'/learn/sdk/{sdk}' + ('#gender' if page.endswith('#gender') else '')


def weekdays(start, taken):
    day = start
    while True:
        if day.weekday() < 5 and day.isoformat() not in taken:
            yield day
        day += timedelta(days=1)


def main():
    catalogue = json.loads(CATALOGUE.read_text(encoding='utf-8'))
    videos = catalogue['videos']
    by_file = {video['file']: video for video in videos}
    taken = {video['publish'] for video in videos if video.get('publish')}
    regular = [video['publish'] for video in videos if video.get('publish') and not video.get('hold')]
    calendar = weekdays(date.fromisoformat(max(regular)) + timedelta(days=1), taken)

    added = []
    for sdk, spec in SDKS.items():
        label = spec['label']
        if sdk not in catalogue['playlists']:
            svelte = catalogue['playlists']['svelte']
            catalogue['playlists'][sdk] = dict(title=svelte['title'].replace('Svelte', label),
                                               description=svelte['description'].replace('Svelte', label))
        longs = [(f'{sdk}/{sdk}-{name}', f'svelte/{name}') for name in LONG]
        shorts = [(f'{sdk}/social/{sdk}-{name}-9x16', f'svelte/social/{name}-9x16') for name in SHORTS]
        queue = []
        while longs or shorts:
            day = next(calendar)
            pool = shorts if day.weekday() in (1, 3) and shorts else longs or shorts
            queue.append((pool.pop(0), day))
        for (file, source), day in queue:
            if file in by_file:
                continue
            original = by_file[source]
            entry = dict(original, file=file, day=spec['day'], publish=day.isoformat(),
                         title=retitle(original['title'], label), page=repage(original['page'], sdk),
                         tags=[spec['tags'].get(tag, tag) for tag in original['tags']])
            if original['playlist'] == 'svelte':
                entry['playlist'] = sdk
            entry.pop('hold', None)
            assert len(entry['title']) <= 100, entry['title']
            videos.append(entry)
            added.append((file, source, label))

    CATALOGUE.write_text(json.dumps(catalogue, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    for path in sorted((YOUTUBE / 'localizations').glob('*.json')):
        strings = json.loads(path.read_text(encoding='utf-8'))
        for file, source, label in added:
            original = strings['videos'][source]
            strings['videos'][file] = dict(original, title=retitle(original['title'], label))
            assert len(strings['videos'][file]['title']) <= 100, (path.name, file)
        path.write_text(json.dumps(strings, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    for file, _, _ in added:
        video = next(v for v in videos if v['file'] == file)
        print(video['publish'], video['playlist'].ljust(6), file.ljust(42), video['title'])


if __name__ == '__main__':
    main()
