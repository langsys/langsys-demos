# Langsys × SvelteKit — starter

A minimal [SvelteKit](https://svelte.dev/docs/kit) app using
[`langsys-js-svelte`](https://github.com/langsys/langsys-js-svelte), seeded on
the server. The live version of the
[SvelteKit guide](https://docs.langsys.dev/learn/guides/sveltekit).

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/langsys/langsys-demos/tree/main/sveltekit)

## Run it

```bash
npm install
npm run dev            # http://localhost:5173, on the shared demo project
```

Pick a language from the menu (the ones the project serves, read on the
server) and watch the page re-translate live. Reload:
the server renders in the locale you picked (a cookie carries it).

## Use your own project

The shared demo project is read-only, so its phrases are translated but one you
write stays in English: a read-only key can't register it. To watch the whole
loop, run the app on a project of your own:

1. At [app.langsys.dev](https://app.langsys.dev), create a project with English
   as the source, a few target languages, and **Automatically AI translate all
   new phrases** turned on.
2. Create a **Read & Write** key for it.
3. In a local clone:

   ```bash
   cp .env.example .env
   ```

   Set `LANGSYS_PROJECT_ID` and `LANGSYS_API_KEY`, and for this experiment set `PUBLIC_LANGSYS_API_KEY` to the
   same write key. The browser is what registers new phrases, so it needs write
   access here; in production that public key must be a read-only one.
4. `npm run dev`, then add a sentence of your own to `src/routes/+page.svelte` with `$t('…', 'Greetings')`
   and reload. It registers, gets translated, and appears in every language you
   picked.

Translating your phrases uses your project's credits. The
[quickstart](https://docs.langsys.dev/learn/quickstart) walks through the same
steps, with a video.

## What's inside

- `src/hooks.server.js` — reads the locale cookie once per request, for the
  load function and for `<html lang>`.
- `src/routes/+layout.server.js` — fetches that locale's catalog with a raw
  `fetch`; SvelteKit serializes it into the page data. The server key never
  reaches the browser.
- `src/routes/+layout.svelte` — a Svelte `writable` is the locale store;
  `LangsysApp.init()` in `onMount` with `initialTranslations` +
  `initialTranslationsLocale`, so the browser doesn't fetch the catalog again.
- `src/routes/+page.svelte` — the plain Svelte SDK from here on: `$t`,
  `<Translate>`, `<Phrase>` and `<DontTranslate>`, the same cards as the Svelte
  demo.

The server fetches the catalog; the SDK translates in the browser. The HTML
the server sends is the base-language text, and the page shows the seeded
locale as soon as it hydrates.

## Learn more

- Guide: [docs.langsys.dev/learn/guides/sveltekit](https://docs.langsys.dev/learn/guides/sveltekit)
- SDK: [`langsys-js-svelte`](https://github.com/langsys/langsys-js-svelte)
