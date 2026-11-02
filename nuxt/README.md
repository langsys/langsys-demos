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

   Set `NUXT_PUBLIC_LANGSYS_PROJECT_ID` and `NUXT_LANGSYS_API_KEY`, and for this experiment set `NUXT_PUBLIC_LANGSYS_API_KEY` to the
   same write key. The browser is what registers new phrases, so it needs write
   access here; in production that public key must be a read-only one.
4. `npm run dev`, then add a sentence of your own to `app/pages/index.vue` with `t('…', 'Greetings')`
   and reload. It registers, gets translated, and appears in every language you
   picked.

Translating your phrases uses your project's credits. The
[quickstart](https://docs.langsys.dev/learn/quickstart) walks through the same
steps, with a video.

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
