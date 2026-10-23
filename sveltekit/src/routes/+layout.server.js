// src/routes/+layout.server.js — step 1 of docs.langsys.dev/learn/guides/sveltekit: the server load
// fetches the catalog once per page render, and SvelteKit serializes it into the page data.
import { env } from '$env/dynamic/private';
import { apiUrl, projectId, serverKey } from '$lib/server/project';

export const load = async ({ fetch, locals }) => {
    const { locale, languages } = locals;
    const res = await fetch(`${apiUrl}/projects/${projectId}/translations?locale=${locale}`, {
        headers: { 'x-Authorization': serverKey },
    });
    // No catalog (bad key, API down): render the source text rather than fail the page.
    const translations = res.ok ? ((await res.json()).data ?? {}) : {};

    return {
        locale,
        languages,
        translations,
        projectId,
        // Which banner the page shows: null when you supplied your own credentials.
        banner: env.LANGSYS_PROJECT_ID ? null : 'shared',
    };
};
