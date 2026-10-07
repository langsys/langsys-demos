import { env } from '$env/dynamic/private';
import { env as publicEnv } from '$env/dynamic/public';
import { DEMO_KEY, DEMO_PROJECT_ID } from '$lib/langsys';

// Your own credentials from .env, else the shared read-only demo project. This key may be a WRITE
// key — it never leaves the server.
export const projectId = env.LANGSYS_PROJECT_ID || DEMO_PROJECT_ID;
export const serverKey = env.LANGSYS_API_KEY || DEMO_KEY;
export const apiUrl = publicEnv.PUBLIC_LANGSYS_API_URL || 'https://api.langsys.dev/api';

// Which languages the project serves — read once every five minutes, not on every render.
let cached = { at: 0, project: null };

export async function getProject(fetch) {
    if (cached.project && Date.now() - cached.at < 300_000) return cached.project;
    try {
        const res = await fetch(`${apiUrl}/authorize-project/${projectId}`, { headers: { 'x-Authorization': serverKey } });
        if (res.ok) cached = { at: Date.now(), project: (await res.json()).data };
    } catch {
        // Unreachable: offer every language rather than fail the page.
    }
    return cached.project;
}
