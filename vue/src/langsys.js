import { LangsysApp, LangsysAppAPI, createLocaleStore } from 'langsys-js-vue';

// One shared locale store: the switcher writes it, LangsysApp reads it.
export const locale = createLocaleStore('en-US');
export const LOCALES = ['en-US', 'es-ES', 'fr-FR', 'de-DE'];

// Friendly names for the locale switcher.
export const LOCALE_LABELS = {
    'en-US': 'English',
    'es-ES': 'Español',
    'fr-FR': 'Français',
    'de-DE': 'Deutsch',
};

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

// Which banner App.vue shows: null when the visitor supplied their own env
// credentials, 'shared' on the public read-only demo project, 'unconfigured'
// when neither exists (nothing will translate).
export const demoBanner = envProjectId ? null : DEMO_PROJECT_ID ? 'shared' : 'unconfigured';

// A READ-ONLY key is safe to ship in a browser app (see .env.example).
LangsysApp.init({
    projectid: envProjectId || DEMO_PROJECT_ID,
    key: import.meta.env.VITE_LANGSYS_API_KEY || DEMO_KEY,
    UserLocaleStore: locale,
});
