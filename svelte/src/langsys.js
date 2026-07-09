import { writable } from 'svelte/store';
import { LangsysApp } from 'langsys-js-svelte';

// A standard Svelte writable is the locale store: the switcher writes it,
// LangsysApp reads it.
export const locale = writable('en-US');
export const LOCALES = ['en-US', 'es-ES', 'fr-FR', 'de-DE'];

// A READ-ONLY key is safe to ship in a browser app (see .env.example).
LangsysApp.init({
    projectid: import.meta.env.VITE_LANGSYS_PROJECT_ID,
    key: import.meta.env.VITE_LANGSYS_API_KEY,
    UserLocaleStore: locale,
});
