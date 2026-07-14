import { LangsysApp, LangsysAppAPI, createSignal } from 'langsys-js-typescript';

// One shared locale store: the switcher writes it, LangsysApp reads it. The
// base SDK's Signal plays the role the framework bindings wrap with hooks,
// composables, or stores.
export const locale = createSignal('en-US');
export const LOCALES = ['en-US', 'es-ES', 'fr-FR', 'de-DE'];

// Friendly names for the locale switcher.
export const LOCALE_LABELS: Record<string, string> = {
    'en-US': 'English',
    'es-ES': 'Español',
    'fr-FR': 'Français',
    'de-DE': 'Deutsch',
};

// Optional: point the SDK at a non-production instance (local dev). Leave unset
// in production and it defaults to api.langsys.dev.
const apiUrl = import.meta.env.VITE_LANGSYS_API_URL;
if (apiUrl) LangsysAppAPI.setBaseUrl(apiUrl);

// A READ-ONLY key is safe to ship in a browser app (see .env.example).
void LangsysApp.init({
    projectid: import.meta.env.VITE_LANGSYS_PROJECT_ID,
    key: import.meta.env.VITE_LANGSYS_API_KEY,
    UserLocaleStore: locale,
});
