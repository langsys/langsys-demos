# Langsys × React — starter

A minimal [Vite](https://vitejs.dev) + React app using
[`langsys-js-react`](https://github.com/langsys/langsys-js-react) for realtime,
continuous translations. The phrase in your code is the lookup key **and** the
base-language default — no keys file, no extraction step.

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/langsys/langsys-demos/tree/main/react)

## Run it

```bash
npm install
cp .env.example .env   # add a READ-ONLY Langsys key + project id
npm run dev
```

Then switch locale with the buttons and watch the page re-translate live.

## What's inside

- `src/langsys.js` — creates the shared locale store and calls `LangsysApp.init()`.
- `src/App.jsx` — the demo: `useT()`, `<Translate>`, `<Phrase>` (with `%name%`
  markup params), and `<DontTranslate>`.

Without a key the app runs in demo mode (source text shows; the switcher still
works). A **read-only** key is safe to ship in a browser app.

## Learn more

- Interactive explorer: the Langsys Learning Center
- SDK: [`langsys-js-react`](https://github.com/langsys/langsys-js-react)
- API docs: [docs.langsys.dev](https://docs.langsys.dev)
