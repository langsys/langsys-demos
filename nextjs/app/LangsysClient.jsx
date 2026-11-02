// app/LangsysClient.jsx — step 2 of docs.langsys.dev/learn/guides/nextjs: initialize the SDK on
// the client with the catalog the server already fetched, so nothing is fetched twice.
'use client';

import { createContext, useContext, useEffect } from 'react';
import { LangsysApp, LangsysAppAPI, useLocaleStore } from 'langsys-js-react';
import { LANGUAGES, LOCALE_COOKIE, pickLanguage } from './langsys';

// One locale store for the whole app, threaded down rather than re-created in each tree.
const LocaleContext = createContext(null);

export function useLocale() {
    return useContext(LocaleContext);
}

export function LangsysClient({ locale, languages, translations, projectId, apiKey, apiUrl, banner, children }) {
    const [selected, setSelected, localeStore] = useLocaleStore(locale);

    useEffect(() => {
        if (apiUrl) LangsysAppAPI.setBaseUrl(apiUrl);
        LangsysApp.init({
            projectid: projectId,
            key: apiKey,
            UserLocaleStore: localeStore,
            initialTranslations: translations,
            initialTranslationsLocale: locale,
            ssrTokenStrategy: 'client',
        });
    }, [localeStore, projectId, apiKey, apiUrl, translations, locale]);

    // Switching fetches the new catalog in the browser; the cookie makes the next server render match.
    const setLocale = (code) => {
        document.cookie = `${LOCALE_COOKIE}=${code}; path=/; max-age=31536000; samesite=lax`;
        // A right-to-left language lays the demo's output out right to left (demo.css).
        document.documentElement.dataset.demoDir = pickLanguage(LANGUAGES, code)?.dir ?? 'ltr';
        setSelected(code);
    };

    return (
        <LocaleContext.Provider value={{ selected, setLocale, languages, banner }}>{children}</LocaleContext.Provider>
    );
}
