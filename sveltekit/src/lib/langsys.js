// Shared by the server load and the components, so it imports nothing from the SDK.

export const LOCALES = ['en-US', 'es-ES', 'fr-FR', 'de-DE'];

// Friendly names for the locale switcher.
export const LOCALE_LABELS = {
    'en-US': 'English',
    'es-ES': 'Español',
    'fr-FR': 'Français',
    'de-DE': 'Deutsch',
};

// The cookie the switcher writes and the server layout reads, so a reload renders the chosen locale.
export const LOCALE_COOKIE = 'langsys_locale';

// Shared public demo project — READ-ONLY key, fixed pre-translated catalog.
// Safe to publish: it can only fetch translations, never register or spend.
// Changing these? Update every copy: typescript/react/vue/svelte/preact/nextjs/nuxt/sveltekit
// (src/langsys.* or the framework's equivalent), laravel (config/langsys.php) and php (index.php).
export const DEMO_PROJECT_ID = '90455431-01d4-47c5-acb8-4fb4fdc6b4f4';
export const DEMO_KEY = 'vAgxOao966WHaxApSBwaLwRlWwZMABmLNHmayhpbAt7JqIpYcybGKms5VGoQ27O0';
