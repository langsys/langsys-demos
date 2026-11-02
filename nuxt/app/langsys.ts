// Shared by the server route and the components, so it imports nothing from the SDK.

export interface Language {
    code: string;
    label: string;
    dir?: 'rtl';
}

// The 18 languages Langsys supports on its own surfaces, each named in itself. The picker offers
// the ones the project serves, on the locale it serves each from (offeredLanguages, below).
// Asking for a locale the project doesn't serve is a 422, which would leave the demo in English.
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

export const languageOf = (code: string) => code.split('-')[0].toLowerCase();

// "es-419" / "zh-hans" / "pt-br" → "es-419" / "zh-Hans" / "pt-BR".
const canonical = (code: string) =>
    code
        .split('-')
        .map((part, i) =>
            i === 0 ? part.toLowerCase() : part.length === 4 ? part[0].toUpperCase() + part.slice(1).toLowerCase() : part.toUpperCase(),
        )
        .join('-');

export interface Project {
    base_locale?: string;
    default_locales?: Record<string, string>;
}

/** The languages a project serves, from its authorize-project data; every one when it couldn't be read. */
export function offeredLanguages(project: Project | null | undefined): Language[] {
    if (!project?.base_locale) return LANGUAGES;
    const served: Record<string, string> = { ...project.default_locales, [languageOf(project.base_locale)]: project.base_locale };
    return LANGUAGES.filter((l) => served[languageOf(l.code)]).map((l) => ({
        ...l,
        code: canonical(served[languageOf(l.code)]),
    }));
}

/** The offered locale in the same language as `code`, if any. */
export function pickLanguage(offered: Language[], code?: string | null): Language | undefined {
    return code ? offered.find((l) => languageOf(l.code) === languageOf(code)) : undefined;
}

// The cookie the switcher writes and the server reads, so a reload renders the chosen locale.
export const LOCALE_COOKIE = 'langsys_locale';
