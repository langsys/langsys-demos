import { Phrase, Translate, currentlyLoadedLocale, t, tSignal } from 'langsys-js-typescript';
import { LOCALES, LOCALE_LABELS, isSharedDemo, locale } from './langsys';
import './hood.css';

/* Shared-demo banner — the read-only default catalog translates existing
   phrases only; make that limitation (and the fix) explicit. */
if (isSharedDemo) {
    const banner = document.createElement('div');
    banner.className = 'demo-banner';
    banner.setAttribute('translate', 'no');
    banner.innerHTML =
        `<strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones won't. ` +
        `Drop your own keys in <code>.env</code> to watch discovery register and translate your phrases live. ` +
        `<a href="https://docs.langsys.dev/learn/concepts/keys-and-environments" target="_blank" rel="noopener noreferrer">Get your keys →</a>`;
    document.body.prepend(banner);
}

// The "look under the hood" page, vanilla edition: the markup lives in
// index.html and this file wires it to langsys-js-typescript directly —
// t() for inline strings, the Translate/Phrase DOM classes for blocks and
// parameterized sentences, and translate="no" for the untouchables.

const app = document.getElementById('app')!;

/* t() — every [data-t] element's own text is its phrase (the key AND the
   default). Capture it once, then re-render through t() whenever tSignal
   re-emits (locale change, catalog load). */
const liveText = [...document.querySelectorAll<HTMLElement>('[data-t]')];
for (const el of liveText) el.dataset.phrase = (el.textContent ?? '').replace(/\s+/g, ' ').trim();

/* X-ray toggle — same phrases, state-dependent label. */
let xray = false;
const xrayButtons = [...document.querySelectorAll<HTMLButtonElement>('[data-xray-toggle]')];
for (const button of xrayButtons) {
    button.addEventListener('click', () => {
        xray = !xray;
        app.classList.toggle('xray', xray);
        for (const b of xrayButtons) b.classList.toggle('on', xray);
        render();
    });
}

function render(): void {
    for (const el of liveText) el.textContent = t(el.dataset.phrase ?? '', 'Site');
    for (const b of xrayButtons) {
        b.textContent = t(xray ? 'Hide the translation layer' : 'Reveal the translation layer', 'Site');
    }
}

// tSignal re-emits a fresh t() whenever translations or the loaded locale
// change — one subscription keeps every inline string current.
tSignal.subscribe(render);

/* Locale switcher pills. */
const nav = document.getElementById('locales')!;
for (const code of LOCALES) {
    const pill = document.createElement('button');
    pill.className = 'pill';
    pill.dataset.locale = code;
    pill.textContent = LOCALE_LABELS[code] ?? code;
    pill.addEventListener('click', () => locale.set(code));
    nav.appendChild(pill);
}
currentlyLoadedLocale.subscribe((loaded) => {
    for (const pill of nav.querySelectorAll<HTMLButtonElement>('.pill')) {
        pill.classList.toggle('active', pill.dataset.locale === (loaded || 'en-US'));
    }
});

/* <Translate> blocks — whole regions of markup, localized as a unit. */
for (const block of document.querySelectorAll<HTMLElement>('[data-translate]')) {
    new Translate(block, { category: 'Site' });
}

/* <Phrase> — one sentence with a dynamic {count}, plural-correct per locale. */
let teams = 1200;
const teamsCount = document.getElementById('teams-count')!;
const teamsPhrase = new Phrase(document.getElementById('teams-phrase')!, {
    category: 'Site',
    params: { count: teams },
});
for (const button of document.querySelectorAll<HTMLButtonElement>('[data-teams]')) {
    button.addEventListener('click', () => {
        teams = Math.max(1, teams + (button.dataset.teams === '+1' ? 1 : -1));
        teamsCount.textContent = String(teams);
        teamsPhrase.setParams({ count: teams });
    });
}
