// Shared public demo project — READ-ONLY key, fixed pre-translated catalog.
// Safe to publish: it can only fetch translations, never register or spend.
// Changing these? Update every copy: typescript/react/vue/svelte/preact/nextjs/nuxt/sveltekit
// (src/langsys.* or the framework's equivalent), laravel (config/langsys.php) and php (index.php).
const DEMO_PROJECT_ID = '90455431-01d4-47c5-acb8-4fb4fdc6b4f4';
const DEMO_KEY = 'vAgxOao966WHaxApSBwaLwRlWwZMABmLNHmayhpbAt7JqIpYcybGKms5VGoQ27O0';

export default defineNuxtConfig({
    compatibilityDate: '2026-10-01',
    css: ['~/assets/demo.css'],
    app: { head: { title: 'Langsys × Nuxt — demo' } },
    // Override any of these from .env (see .env.example): NUXT_LANGSYS_API_KEY,
    // NUXT_PUBLIC_LANGSYS_PROJECT_ID, and so on.
    runtimeConfig: {
        // Server-only: may be a WRITE key — it never reaches the browser.
        langsysApiKey: DEMO_KEY,
        public: {
            langsysProjectId: DEMO_PROJECT_ID,
            langsysApiKey: DEMO_KEY, // read-only — ships to the browser
            langsysApiUrl: 'https://api.langsys.dev/api',
            // Which banner the page shows: true until you configure your own project.
            langsysSharedDemo: !process.env.NUXT_PUBLIC_LANGSYS_PROJECT_ID,
        },
    },
    // Pre-bundle the SDK at server start. Without this, Vite optimizes it
    // mid-first-load and fires a reload StackBlitz's preview can miss,
    // leaving the app stuck until a manual refresh.
    vite: { optimizeDeps: { include: ['langsys-js-vue'] } },
});
