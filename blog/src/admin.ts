import { DRAFT, publish } from './posts';
import './journal.css';

// The CMS side. It never loads Langsys: publishing a post is the writer's whole
// job, and nothing about it involves a developer or a deploy.

const form = document.querySelector<HTMLFormElement>('#editor')!;
const title = form.querySelector<HTMLInputElement>('#title')!;
const body = form.querySelector<HTMLTextAreaElement>('#body')!;
const done = document.querySelector<HTMLElement>('#published')!;

body.value = DRAFT.body.join('\n\n');

form.addEventListener('submit', (event) => {
    event.preventDefault();
    const paragraphs = body.value
        .split(/\n\s*\n/)
        .map((text) => text.trim())
        .filter(Boolean);
    const post = publish(title.value.trim() || DRAFT.title, paragraphs);
    const link = done.querySelector<HTMLAnchorElement>('a')!;
    link.href = `/post.html?p=${post.slug}`;
    link.textContent = `${location.host}/post.html?p=${post.slug}`;
    done.hidden = false;
    form.querySelector<HTMLButtonElement>('button[type=submit]')!.textContent = 'Published';
});
