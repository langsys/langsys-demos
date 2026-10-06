export const LOCALES = ['en-US', 'es-ES', 'fr-FR', 'de-DE'];

// Friendly names for the locale switcher.
export const LOCALE_LABELS: Record<string, string> = {
    'en-US': 'English',
    'es-ES': 'Español',
    'fr-FR': 'Français',
    'de-DE': 'Deutsch',
};

// The cookie the switcher writes and the server reads, so a reload renders the chosen locale.
export const LOCALE_COOKIE = 'langsys_locale';
