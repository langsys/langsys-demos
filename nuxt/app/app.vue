<!-- app/app.vue — step 2 of docs.langsys.dev/learn/guides/nuxt: useAsyncData runs the fetch on the
     server and serializes it into the page, so the client initializes from it without refetching. -->
<script setup lang="ts">
import { LangsysApp, LangsysAppAPI, createLocaleStore } from 'langsys-js-vue';
import type { iCategories } from 'langsys-js-vue';
import { LOCALES, LOCALE_COOKIE } from './langsys';

// From the cookie the switcher writes; a first visit gets English.
const cookie = useCookie(LOCALE_COOKIE, { maxAge: 31536000, sameSite: 'lax' });
const initial = LOCALES.includes(cookie.value ?? '') ? cookie.value! : 'en-US';

const { data } = await useAsyncData('langsys', () => $fetch('/api/langsys', { query: { locale: initial } }));

useHead({ htmlAttrs: { lang: initial } });

// One locale store for the app, provided to every page below.
const store = createLocaleStore(data.value!.locale);
provide('locale', store);

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
    });
});
</script>

<template>
    <NuxtPage />
</template>
