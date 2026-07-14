import { writable } from 'svelte/store';
import { LangsysApp, LangsysAppAPI } from 'langsys-js-svelte';

// A standard Svelte writable is the locale store: the switcher writes it,
// LangsysApp reads it.
export const locale = writable('en-US');
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
// Changing these? Update the langsys.js in all four demo apps.
const DEMO_PROJECT_ID = '';
const DEMO_KEY = '';

const envProjectId = import.meta.env.VITE_LANGSYS_PROJECT_ID;

// True when running on the shared demo project instead of the visitor's own —
// drives the read-only banner in App.svelte.
export const isSharedDemo = !envProjectId && Boolean(DEMO_PROJECT_ID);

// A READ-ONLY key is safe to ship in a browser app (see .env.example).
LangsysApp.init({
    projectid: envProjectId || DEMO_PROJECT_ID,
    key: import.meta.env.VITE_LANGSYS_API_KEY || DEMO_KEY,
    UserLocaleStore: locale,
});
