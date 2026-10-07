<!-- app/app.vue — step 2 of docs.langsys.dev/learn/guides/nuxt: useAsyncData runs the fetch on the
     server and serializes it into the page, so the client initializes from it without refetching. -->
<script setup lang="ts">
import { LangsysApp, LangsysAppAPI, createLocaleStore } from 'langsys-js-vue';
import type { iCategories } from 'langsys-js-vue';
import { LANGUAGES, LOCALE_COOKIE, pickLanguage } from './langsys';

// From the cookie the switcher writes; the server route keeps it only if the project serves that
// language, and answers with the locale it resolved and the languages on offer.
const cookie = useCookie(LOCALE_COOKIE, { maxAge: 31536000, sameSite: 'lax' });

const { data } = await useAsyncData('langsys', () => $fetch('/api/langsys', { query: { locale: cookie.value } }));
const dirOf = (code: string) => pickLanguage(LANGUAGES, code)?.dir ?? 'ltr';

useHead({ htmlAttrs: { lang: data.value!.locale, 'data-demo-dir': dirOf(data.value!.locale) } });

// One locale store for the app, and the languages on offer, provided to every page below.
const store = createLocaleStore(data.value!.locale);
provide('locale', store);
provide('languages', data.value!.languages);

onMounted(() => {
    const config = useRuntimeConfig().public;
    LangsysAppAPI.setBaseUrl(config.langsysApiUrl);
    LangsysApp.init({
        projectid: config.langsysProjectId,
        key: config.langsysApiKey, // read-only
        UserLocaleStore: store,
        initialTranslations: data.value!.translations as iCategories,
        initialTranslationsLocale: data.value!.locale,
        ssrTokenStrategy: 'client',
    });

    // Switching fetches the new catalog in the browser; the cookie makes the next server render match.
    // Only on a switch: the first call is the locale the server already rendered.
    let first = true;
    store.subscribe((code) => {
        if (first) return void (first = false);
        cookie.value = code;
        // A right-to-left language lays the demo's output out right to left (demo.css).
        document.documentElement.dataset.demoDir = dirOf(code);
    });
});
</script>

<template>
    <NuxtPage />
</template>
