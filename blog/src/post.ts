import { Translate } from 'langsys-js-typescript';
import { configured, mountLanguagePicker, mountWirePanel, start } from './langsys';
import { findPost, formatDate } from './posts';
import './journal.css';

// The panel has to be watching fetch before the SDK makes its first call.
mountWirePanel(document.querySelector<HTMLElement>('#wire')!);
mountLanguagePicker(document.querySelector<HTMLSelectElement>('#locale-select')!);

const slug = new URLSearchParams(location.search).get('p') ?? '';
const post = findPost(slug);
const article = document.querySelector<HTMLElement>('#post')!;
const meta = document.querySelector<HTMLElement>('#meta')!;

if (post) {
    document.title = `${post.title} · Selvara Journal`;
    meta.textContent = formatDate(post.published);
    const title = document.createElement('h1');
    title.textContent = post.title;
    article.append(title, ...post.body.map((text) => Object.assign(document.createElement('p'), { textContent: text })));

    // The whole post is one content block: whatever the CMS put in it is
    // translated as a unit, and nobody wrote a key for any of it.
    new Translate(article, { category: 'Blog' });
} else {
    article.innerHTML = '<h1>Post not found</h1><p><a href="/">Back to the journal</a></p>';
}

if (!configured) {
    document.querySelector<HTMLElement>('#wire')!.dataset.unconfigured = '';
}

start();
