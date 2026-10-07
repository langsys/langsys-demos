<!-- src/routes/+layout.svelte — step 2 of docs.langsys.dev/learn/guides/sveltekit: initialize on the
     client with the catalog the server load already fetched, so nothing is fetched twice. -->
<script>
    import { onMount, setContext } from 'svelte';
    import { writable } from 'svelte/store';
    import { LangsysApp, LangsysAppAPI } from 'langsys-js-svelte';
    import { env } from '$env/dynamic/public';
    import { DEMO_KEY, LOCALE_COOKIE } from '$lib/langsys';
    import '$lib/demo.css';

    export let data;

    // A standard Svelte writable is the locale store — the binding adapts it for the SDK. Shared
    // through context so the page's switcher writes the same one.
    const locale = writable(data.locale);
    setContext('locale', locale);

    onMount(() => {
        if (env.PUBLIC_LANGSYS_API_URL) LangsysAppAPI.setBaseUrl(env.PUBLIC_LANGSYS_API_URL);
        LangsysApp.init({
            projectid: data.projectId,
            key: env.PUBLIC_LANGSYS_API_KEY || DEMO_KEY, // read-only
            UserLocaleStore: locale,
            initialTranslations: data.translations,
            initialTranslationsLocale: data.locale,
            ssrTokenStrategy: 'client',
        });

        // Switching fetches the new catalog in the browser; the cookie makes the next server render match.
        // Only on a switch: the first call is the locale the server already rendered.
        let first = true;
        return locale.subscribe((code) => {
            if (first) return void (first = false);
            document.cookie = `${LOCALE_COOKIE}=${code}; path=/; max-age=31536000; samesite=lax`;
        });
    });
</script>

<slot />
