// server/api/langsys.get.ts — step 1 of docs.langsys.dev/learn/guides/nuxt: a Nitro route fetches
// the catalog, so the server key stays in private runtime config. The browser only ever talks to
// this route, and only during SSR.
import { offeredLanguages, pickLanguage, type Project } from '../../app/langsys';

// Which languages the project serves — read once every five minutes, not on every render.
let cached: { at: number; project: Project | null } = { at: 0, project: null };

async function getProject(apiUrl: string, projectId: string, key: string) {
    if (cached.project && Date.now() - cached.at < 300_000) return cached.project;
    try {
        const res = await $fetch<{ data: Project }>(`${apiUrl}/authorize-project/${projectId}`, {
            headers: { 'x-Authorization': key },
        });
        cached = { at: Date.now(), project: res.data };
    } catch {
        // Unreachable: offer every language rather than fail the page.
    }
    return cached.project;
}

export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig();
    const { langsysApiUrl: apiUrl, langsysProjectId: projectId } = config.public;
    const languages = offeredLanguages(await getProject(apiUrl, projectId, config.langsysApiKey));
    // The requested locale if the project serves that language; else English.
    const locale = pickLanguage(languages, getQuery(event).locale as string)?.code ?? 'en-US';
    try {
        const res = await $fetch<{ data: unknown }>(`${apiUrl}/projects/${projectId}/translations`, {
            query: { locale },
            headers: { 'x-Authorization': config.langsysApiKey },
        });
        return { locale, languages, translations: res.data ?? {} };
    } catch {
        // No catalog (bad key, API down): render the source text rather than fail the page.
        return { locale, languages, translations: {} };
    }
});
