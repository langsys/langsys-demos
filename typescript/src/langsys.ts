import { LangsysApp, LangsysAppAPI, canonicalizeLocale, createSignal } from 'langsys-js-typescript';

// One shared locale store: the switcher writes it, LangsysApp reads it. The
// base SDK's Signal plays the role the framework bindings wrap with hooks,
// composables, or stores.
export const locale = createSignal('en-US');

// The 18 languages Langsys supports on its own surfaces, each named in itself. The picker
// offers the ones the project serves, on the locale it serves each from — read from the
// project once the SDK has started (end of this file). Asking for a locale the project
// doesn't serve is a 422, which would leave the demo silently in English.
export interface Language {
    code: string;
    label: string;
    dir?: 'rtl';
}

export const LANGUAGES: Language[] = [
    { code: 'en-US', label: 'English' },
    { code: 'es-419', label: 'Español' },
    { code: 'pt-BR', label: 'Português' },
    { code: 'fr-FR', label: 'Français' },
    { code: 'de-DE', label: 'Deutsch' },
    { code: 'it-IT', label: 'Italiano' },
    { code: 'ja-JP', label: '日本語' },
    { code: 'zh-Hans', label: '中文' },
    { code: 'ko-KR', label: '한국어' },
    { code: 'ru-RU', label: 'Русский' },
    { code: 'uk-UA', label: 'Українська' },
    { code: 'tr-TR', label: 'Türkçe' },
    { code: 'pl-PL', label: 'Polski' },
    { code: 'nl-NL', label: 'Nederlands' },
    { code: 'id-ID', label: 'Bahasa Indonesia' },
    { code: 'vi-VN', label: 'Tiếng Việt' },
    { code: 'hi-IN', label: 'हिन्दी' },
    { code: 'ar-001', label: 'العربية', dir: 'rtl' },
];

export const languages = createSignal<Language[]>(LANGUAGES);

const languageOf = (code: string) => code.split('-')[0].toLowerCase();

// Optional: point the SDK at a non-production instance (local dev). Leave unset
// in production and it defaults to api.langsys.dev.
const apiUrl = import.meta.env.VITE_LANGSYS_API_URL;
if (apiUrl) LangsysAppAPI.setBaseUrl(apiUrl);

// Shared public demo project — READ-ONLY key, fixed pre-translated catalog.
// Safe to publish: it can only fetch translations, never register or spend.
// Changing these? Update all six copies: typescript/react/vue/svelte/preact
// (src/langsys.*) and laravel (config/langsys.php).
const DEMO_PROJECT_ID = '90455431-01d4-47c5-acb8-4fb4fdc6b4f4';
const DEMO_KEY = 'vAgxOao966WHaxApSBwaLwRlWwZMABmLNHmayhpbAt7JqIpYcybGKms5VGoQ27O0';

const envProjectId = import.meta.env.VITE_LANGSYS_PROJECT_ID;

// Which banner main.ts shows: null when the visitor supplied their own env
// credentials, 'shared' on the public read-only demo project, 'unconfigured'
// when neither exists (nothing will translate).
export const demoBanner: 'shared' | 'unconfigured' | null = envProjectId
    ? null
    : DEMO_PROJECT_ID
      ? 'shared'
      : 'unconfigured';

// A READ-ONLY key is safe to ship in a browser app (see .env.example).
LangsysApp.init({
    projectid: envProjectId || DEMO_PROJECT_ID,
    key: import.meta.env.VITE_LANGSYS_API_KEY || DEMO_KEY,
    UserLocaleStore: locale,
}).then((response) => {
    type Project = { base_locale?: string; default_locales?: Record<string, string> };
    const project = (response as { data?: Project })?.data;
    if (!project?.base_locale) return;
    const served: Record<string, string> = { ...project.default_locales, [languageOf(project.base_locale)]: project.base_locale };
    const offered = LANGUAGES.filter((l) => served[languageOf(l.code)]).map((l) => ({
        ...l,
        code: canonicalizeLocale(served[languageOf(l.code)]),
    }));
    languages.set(offered);
    // Keep the selected language, on the locale the project serves it from.
    const selected = offered.find((l) => languageOf(l.code) === languageOf(locale.get()));
    locale.set(selected?.code ?? 'en-US');
});

// A right-to-left language lays the demo's output out right to left (demo.css).
locale.subscribe((code: string) => {
    document.documentElement.dataset.demoDir =
        LANGUAGES.find((l) => languageOf(l.code) === languageOf(code))?.dir ?? 'ltr';
});
