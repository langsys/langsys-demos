import { LangsysApp, createLocaleStore } from 'langsys-js-vue';

// One shared locale store: the switcher writes it, LangsysApp reads it.
export const locale = createLocaleStore('en-US');
export const LOCALES = ['en-US', 'es-ES', 'fr-FR', 'de-DE'];

// A READ-ONLY key is safe to ship in a browser app (see .env.example).
LangsysApp.init({
    projectid: import.meta.env.VITE_LANGSYS_PROJECT_ID,
    key: import.meta.env.VITE_LANGSYS_API_KEY,
    UserLocaleStore: locale,
});
