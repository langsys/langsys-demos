// server/api/langsys.get.ts — step 1 of docs.langsys.dev/learn/guides/nuxt: a Nitro route fetches
// the catalog, so the server key stays in private runtime config. The browser only ever talks to
// this route, and only during SSR.
export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig();
    const locale = (getQuery(event).locale as string) ?? 'en-US';
    try {
        const res = await $fetch<{ data: unknown }>(
            `${config.public.langsysApiUrl}/projects/${config.public.langsysProjectId}/translations`,
            { query: { locale }, headers: { 'x-Authorization': config.langsysApiKey } },
        );
        return { locale, translations: res.data ?? {} };
    } catch {
        // No catalog (bad key, API down): render the source text rather than fail the page.
        return { locale, translations: {} };
    }
});
