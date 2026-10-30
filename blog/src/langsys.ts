import { LangsysApp, LangsysAppAPI, canonicalizeLocale, createSignal, writeEnabled } from 'langsys-js-typescript';

// The two languages the journal offers. The project may serve more; the
// picker shows these on whichever locale the project serves each from.
const OFFERED = [
    { code: 'en-US', label: 'English' },
    { code: 'es-ES', label: 'Español' },
];

const LOCALE_STORE = 'selvara-journal-locale';

function savedLocale(): string {
    try {
        return localStorage.getItem(LOCALE_STORE) ?? 'en-US';
    } catch {
        return 'en-US';
    }
}

export const locale = createSignal(savedLocale());
export const languages = createSignal(OFFERED);

locale.subscribe((code: string) => {
    try {
        localStorage.setItem(LOCALE_STORE, code);
    } catch {
        // Private mode: the choice lasts until the page closes.
    }
});

const languageOf = (code: string) => code.split('-')[0].toLowerCase();

const apiUrl = import.meta.env.VITE_LANGSYS_API_URL;
if (apiUrl) LangsysAppAPI.setBaseUrl(apiUrl);

export const configured = Boolean(import.meta.env.VITE_LANGSYS_PROJECT_ID && import.meta.env.VITE_LANGSYS_API_KEY);

export function start(): void {
    if (!configured) return;
    LangsysApp.init({
        projectid: import.meta.env.VITE_LANGSYS_PROJECT_ID,
        key: import.meta.env.VITE_LANGSYS_API_KEY,
        UserLocaleStore: locale,
    }).then((response) => {
        type Project = { base_locale?: string; default_locales?: Record<string, string> };
        const project = (response as { data?: Project })?.data;
        if (!project?.base_locale) return;
        const served: Record<string, string> = { ...project.default_locales, [languageOf(project.base_locale)]: project.base_locale };
        const offered = OFFERED.filter((l) => served[languageOf(l.code)]).map((l) => ({
            ...l,
            code: canonicalizeLocale(served[languageOf(l.code)]),
        }));
        languages.set(offered);
        const selected = offered.find((l) => languageOf(l.code) === languageOf(locale.get()));
        locale.set(selected?.code ?? offered[0]?.code ?? 'en-US');
    });
}

export function mountLanguagePicker(select: HTMLSelectElement): void {
    select.addEventListener('change', () => locale.set(select.value));
    const render = () => {
        select.replaceChildren(...languages.get().map((l) => new Option(l.label, l.code)));
        select.value = languages.get().find((l) => languageOf(l.code) === languageOf(locale.get()))?.code ?? '';
    };
    languages.subscribe(render);
    locale.subscribe(render);
}

/* "This browser and Langsys": the panel in the corner of a post. It answers the
   two things the video is about with what actually happened, not a claim. The
   write answer is the SDK's own `writeEnabled`, which the server decides from
   the address asking. The requests are the SDK's own calls, read off fetch as
   they leave, with nothing added or summarized beyond the item count. */
export function mountWirePanel(panel: HTMLElement): void {
    const answer = panel.querySelector<HTMLElement>('[data-write]')!;
    const log = panel.querySelector<HTMLElement>('[data-log]')!;

    writeEnabled.subscribe((enabled) => {
        answer.dataset.state = enabled === undefined ? 'asking' : enabled ? 'yes' : 'no';
        answer.textContent =
            enabled === undefined
                ? 'Asking Langsys…'
                : enabled
                  ? 'Yes: this address is on the key’s allowlist'
                  : 'No: read-only from this address';
    });

    const add = (method: string, path: string, detail: string) => {
        const row = document.createElement('li');
        const head = document.createElement('code');
        head.textContent = `${method} /${path}`;
        const text = document.createElement('span');
        text.textContent = detail;
        row.append(head, text);
        log.append(row);
        panel.classList.add('has-log');
    };

    const original = window.fetch.bind(window);
    window.fetch = (input: RequestInfo | URL, init?: RequestInit) => {
        const url = typeof input === 'string' ? input : input instanceof URL ? input.href : input.url;
        const method = (init?.method ?? 'GET').toUpperCase();
        const path = url.replace(/^.*\/api\//, '').split('?')[0];
        if (method === 'POST' && path === 'discovery/hint') {
            const body = JSON.parse(String(init?.body ?? '{}')) as { page_url?: string };
            add(method, path, `The page address, ${body.page_url}. Nothing else.`);
        } else if (method === 'POST' && path === 'translatable-items') {
            const body = JSON.parse(String(init?.body ?? '{}')) as { translatable_items?: unknown[] };
            const count = body.translatable_items?.length ?? 0;
            add(method, path, `This post, registered: ${count} ${count === 1 ? 'item' : 'items'}.`);
        }
        return original(input, init);
    };
}
