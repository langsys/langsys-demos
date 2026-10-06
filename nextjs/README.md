# Langsys × Next.js — starter

A minimal [Next.js](https://nextjs.org) App Router app using
[`langsys-js-react`](https://github.com/langsys/langsys-js-react), seeded on the
server. The live version of the
[Next.js guide](https://docs.langsys.dev/learn/guides/nextjs).

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/langsys/langsys-demos/tree/main/nextjs)

## Run it

```bash
npm install
npm run dev            # http://localhost:3000, on the shared demo project
```

Switch locale with the buttons and watch the page re-translate live. Reload:
the server renders in the locale you picked (a cookie carries it).

## What's inside

- `app/layout.jsx` — Server Component: reads the locale cookie and fetches that
  locale's catalog with a raw `fetch`. The server key never reaches the browser.
- `app/LangsysClient.jsx` — `'use client'` wrapper: `LangsysApp.init()` with
  `initialTranslations` + `initialTranslationsLocale`, so the browser doesn't
  fetch the catalog again; owns the one locale store for the app.
- `app/Demo.jsx` — the plain React SDK from here on: `useT()`, `<Translate>`,
  `<Phrase>` and `<DontTranslate>`, the same cards as the React demo.

The server fetches the catalog; the SDK translates in the browser. The HTML
the server sends is the base-language text, and the page shows the seeded
locale as soon as it hydrates.

## Learn more

- Guide: [docs.langsys.dev/learn/guides/nextjs](https://docs.langsys.dev/learn/guides/nextjs)
- SDK: [`langsys-js-react`](https://github.com/langsys/langsys-js-react)
