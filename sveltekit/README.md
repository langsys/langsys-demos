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
