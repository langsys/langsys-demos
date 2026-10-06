// src/routes/+layout.server.js — step 1 of docs.langsys.dev/learn/guides/sveltekit: the server load
// fetches the catalog once per page render, and SvelteKit serializes it into the page data.
import { env } from '$env/dynamic/private';
import { env as publicEnv } from '$env/dynamic/public';
import { DEMO_KEY, DEMO_PROJECT_ID } from '$lib/langsys';

// Your own credentials from .env, else the shared read-only demo project. This key may be a WRITE
// key — it never leaves the server.
const projectId = env.LANGSYS_PROJECT_ID || DEMO_PROJECT_ID;
const serverKey = env.LANGSYS_API_KEY || DEMO_KEY;
const apiUrl = publicEnv.PUBLIC_LANGSYS_API_URL || 'https://api.langsys.dev/api';

export const load = async ({ fetch, locals }) => {
    const { locale } = locals;
    const res = await fetch(`${apiUrl}/projects/${projectId}/translations?locale=${locale}`, {
        headers: { 'x-Authorization': serverKey },
    });
    // No catalog (bad key, API down): render the source text rather than fail the page.
    const translations = res.ok ? ((await res.json()).data ?? {}) : {};

    return {
        locale,
        translations,
        projectId,
        // Which banner the page shows: null when you supplied your own credentials.
        banner: env.LANGSYS_PROJECT_ID ? null : 'shared',
    };
};
