/**
 * Shared public demo project — READ-ONLY key, fixed pre-translated catalog.
 * Safe to publish: it can only fetch translations, never register or spend.
 * Changing these? Update all copies: typescript/react/vue/svelte/preact
 * (src/langsys.*), laravel + symfony (config), nestjs + hono (this pattern).
 */
const DEMO_PROJECT_ID = '90455431-01d4-47c5-acb8-4fb4fdc6b4f4';
const DEMO_KEY = 'vAgxOao966WHaxApSBwaLwRlWwZMABmLNHmayhpbAt7JqIpYcybGKms5VGoQ27O0';

export const projectid = process.env.LANGSYS_PROJECT_ID || DEMO_PROJECT_ID;
export const key = process.env.LANGSYS_API_KEY || DEMO_KEY;
export const apiUrl = process.env.LANGSYS_API_URL || undefined;

/**
 * Which banner the page shows: null when the visitor supplied their own
 * credentials, 'shared' on the public read-only demo project, 'unconfigured'
 * when neither exists (only possible if the baked defaults are blanked).
 */
export const banner: 'shared' | 'unconfigured' | null = process.env.LANGSYS_PROJECT_ID
    ? null
    : projectid
      ? 'shared'
      : 'unconfigured';

export const LOCALES: Record<string, string> = {
    'en-US': 'English',
    'es-ES': 'Español',
    'fr-FR': 'Français',
    'de-DE': 'Deutsch',
};
