import { createLocaleStore } from 'langsys-js-angular';
import type { LangsysConfig } from 'langsys-js-angular';

// One shared locale store: the switcher writes it, LangsysApp reads it.
// `locale.locale` is an Angular signal (read it in templates); the store itself
// is what the SDK subscribes to, so it goes straight into the config.
export const locale = createLocaleStore('en-US');
export const LOCALES = ['en-US', 'es-ES', 'fr-FR', 'de-DE'];

// Friendly names for the locale switcher.
export const LOCALE_LABELS: Record<string, string> = {
    'en-US': 'English',
    'es-ES': 'Español',
    'fr-FR': 'Français',
    'de-DE': 'Deutsch',
};

// Read build-time env the same way the other demos do. The Angular CLI (unlike
// Vite) doesn't define `import.meta.env`, so we read it defensively — set these
// in an Angular `environment.ts`, or just edit the DEMO_* constants below.
const env = ((import.meta as unknown as { env?: Record<string, string | undefined> }).env ?? {}) as Record<
    string,
    string | undefined
>;

// Optional: point the SDK at a non-production instance (local dev). Leave unset
// in production and it defaults to api.langsys.dev.
const apiUrl = env['VITE_LANGSYS_API_URL'];

// Shared public demo project — READ-ONLY key, fixed pre-translated catalog.
// Safe to publish: it can only fetch translations, never register or spend.
// Changing these? Update the langsys.js/.ts in all demo apps.
const DEMO_PROJECT_ID = '90455431-01d4-47c5-acb8-4fb4fdc6b4f4';
const DEMO_KEY = 'vAgxOao966WHaxApSBwaLwRlWwZMABmLNHmayhpbAt7JqIpYcybGKms5VGoQ27O0';

const envProjectId = env['VITE_LANGSYS_PROJECT_ID'];

// Which banner App shows: null when the visitor supplied their own env
// credentials, 'shared' on the public read-only demo project, 'unconfigured'
// when neither exists (nothing will translate).
export const demoBanner: 'shared' | 'unconfigured' | null = envProjectId
    ? null
    : DEMO_PROJECT_ID
      ? 'shared'
      : 'unconfigured';

// A READ-ONLY key is safe to ship in a browser app (see .env.example).
// Passed to provideLangsys() in main.ts. `blockUntilReady: false` lets the app
// paint immediately (source text) even with no/slow credentials — right for a demo.
export const langsysConfig: LangsysConfig = {
    projectid: envProjectId || DEMO_PROJECT_ID,
    key: env['VITE_LANGSYS_API_KEY'] || DEMO_KEY,
    apiUrl,
    UserLocaleStore: locale,
    initialLocale: 'en-US',
    blockUntilReady: false,
};
