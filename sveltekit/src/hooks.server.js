import { LANGUAGES, LOCALE_COOKIE, offeredLanguages, pickLanguage } from '$lib/langsys';
import { getProject } from '$lib/server/project';

// The visitor's locale, from the cookie the switcher writes if the project serves that language;
// a first visit gets English. Resolved once per request, for the load function and for <html>.
export async function handle({ event, resolve }) {
    const languages = offeredLanguages(await getProject(event.fetch));
    const locale = pickLanguage(languages, event.cookies.get(LOCALE_COOKIE))?.code ?? 'en-US';
    event.locals.languages = languages;
    event.locals.locale = locale;

    return resolve(event, {
        transformPageChunk: ({ html }) =>
            html.replace('%lang%', locale).replace('%demo-dir%', pickLanguage(LANGUAGES, locale)?.dir ?? 'ltr'),
    });
}
