# Langsys × Nuxt — starter

A minimal [Nuxt](https://nuxt.com) app using
[`langsys-js-vue`](https://github.com/langsys/langsys-js-vue), seeded on the
server. The live version of the
[Nuxt guide](https://docs.langsys.dev/learn/guides/nuxt).

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/langsys/langsys-demos/tree/main/nuxt)

## Run it

Node 22.12 or later.

```bash
npm install
npm run dev            # http://localhost:3000, on the shared demo project
```

Switch locale with the buttons and watch the page re-translate live. Reload:
the server renders in the locale you picked (a cookie carries it).

## What's inside

- `server/api/langsys.get.ts` — a Nitro route fetches the catalog, so the
  server key stays in private runtime config.
- `app/app.vue` — `useAsyncData` calls that route during SSR and serializes the
  result into the page; `LangsysApp.init()` in `onMounted` with
  `initialTranslations` + `initialTranslationsLocale`, so the browser doesn't
  fetch the catalog again. Provides the one locale store to every page.
- `app/pages/index.vue` — the plain Vue SDK from here on: `useT()`,
  `<Translate>`, `<Phrase>` and `<DontTranslate>`, the same cards as the Vue
  demo.

The server fetches the catalog; the SDK translates in the browser. The HTML
the server sends is the base-language text, and the page shows the seeded
locale as soon as it hydrates.

## Learn more

- Guide: [docs.langsys.dev/learn/guides/nuxt](https://docs.langsys.dev/learn/guides/nuxt)
- SDK: [`langsys-js-vue`](https://github.com/langsys/langsys-js-vue)
