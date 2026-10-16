import { Phrase, Translate, currentlyLoadedLocale, t, tSignal } from 'langsys-js-typescript';
import { demoBanner, languages, locale } from './langsys';
import './demo.css';

/* Demo banner — on the shared read-only project, the default catalog
   translates existing phrases only; with no credentials at all, nothing
   translates. Make whichever limitation applies (and the fix) explicit. */
if (demoBanner) {
    const message =
        demoBanner === 'shared'
            ? `<strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones won't. ` +
              `Drop your own keys in <code>.env</code> to watch discovery register and translate your phrases live. `
            : `<strong>No Langsys credentials configured</strong> — showing source text only, nothing translates. ` +
              `Add your project id and key in <code>.env</code> to see it live. `;
    const banner = document.createElement('div');
    banner.className = 'demo-banner';
    banner.setAttribute('translate', 'no');
    banner.innerHTML =
        message +
        `<a href="https://docs.langsys.dev/learn/concepts/keys-and-environments" target="_blank" rel="noopener noreferrer">Get your keys →</a>`;
    document.body.prepend(banner);
}

// The vanilla demo app: every example on docs.langsys.dev/learn/sdk/typescript
// running live, wired by the exact code the docs page shows.

/* t() — inline string, wired to the DOM. tSignal re-emits a fresh t()
   whenever the locale or catalog changes — subscribe once and the element
   stays translated. */
const greeting = document.querySelector<HTMLElement>('#greeting')!;
const name = 'Sarah';

tSignal.subscribe(() => {
    greeting.textContent = t('Hello, {name}!', 'Greetings', { name });
});

/* t() — plurals. The phrase is written flat; Langsys generates the plural
   forms per locale (the base locale included) and the SDK picks the branch
   from `count`. Nobody types ICU. */
const inbox = document.querySelector<HTMLElement>('#inbox')!;
const inboxCount = document.querySelector<HTMLElement>('#inbox-count')!;
let messages = 3;

const renderInbox = (): void => {
    inboxCount.textContent = String(messages);
    inbox.textContent = t(
        'Hello, {name}! You have {count} new messages.',
        'Greetings',
        { name, count: messages },
    );
};
tSignal.subscribe(renderInbox);
document.querySelector('#inbox-minus')!.addEventListener('click', () => {
    messages = Math.max(0, messages - 1);
    renderInbox();
});
document.querySelector('#inbox-plus')!.addEventListener('click', () => {
    messages += 1;
    renderInbox();
});

/* Translate — a whole content block, localized as a single unit. */
new Translate(document.querySelector<HTMLElement>('#hero')!, { category: 'Home' });

/* Phrase — one sentence with dynamic params; the element's own text holds
   the {name}/{count} placeholders. */
let items = 3;
const cartCount = document.querySelector<HTMLElement>('#cart-count')!;
const cartNote = new Phrase(document.querySelector<HTMLElement>('#cart-note')!, {
    category: 'Cart',
    params: { name: 'Sarah', count: items },
});
document.querySelector('#cart-minus')!.addEventListener('click', () => {
    items = Math.max(0, items - 1);
    cartCount.textContent = String(items);
    cartNote.setParams({ name: 'Sarah', count: items });
});
document.querySelector('#cart-plus')!.addEventListener('click', () => {
    items += 1;
    cartCount.textContent = String(items);
    cartNote.setParams({ name: 'Sarah', count: items });
});

/* translate="no" — the tokenizer and renderer skip the marked subtree, so it
   stays verbatim while the sentence around it translates. */
new Translate(document.querySelector<HTMLElement>('#signin')!, { category: 'Tour' });

/* Language picker — the languages the project serves, rebuilt when the SDK has read them. */
const select = document.querySelector<HTMLSelectElement>('#locale-select')!;
select.addEventListener('change', () => locale.set(select.value));
languages.subscribe((list) => {
    select.replaceChildren(...list.map((l) => new Option(l.label, l.code)));
    select.value = locale.get();
});
locale.subscribe((code) => {
    if (select.value !== code) select.value = code;
});

/* Reading signals — currentlyLoadedLocale tracks the catalog actually loaded. */
const meta = document.getElementById('locale-meta')!;
currentlyLoadedLocale.subscribe((loaded) => {
    meta.textContent = `loaded ${loaded || 'en-US'}`;
});
