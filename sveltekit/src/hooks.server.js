import { LOCALES, LOCALE_COOKIE } from '$lib/langsys';

// The visitor's locale, from the cookie the switcher writes; a first visit gets English.
// Resolved once per request, for the load function and for <html lang>.
export async function handle({ event, resolve }) {
    const saved = event.cookies.get(LOCALE_COOKIE);
    event.locals.locale = LOCALES.includes(saved) ? saved : 'en-US';

    return resolve(event, {
        transformPageChunk: ({ html }) => html.replace('%lang%', event.locals.locale),
    });
}
