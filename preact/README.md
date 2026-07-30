# Langsys × Preact — starter

A minimal [Vite](https://vitejs.dev) + Preact app using
[`langsys-js-react`](https://github.com/langsys/langsys-js-react) — yes, the
**React** SDK — through `preact/compat`. The app code is the React demo's
`App.jsx`, verbatim: the SDK imports only `useSyncExternalStore`, `useState`,
`useRef`, `useEffect`, and `createElement`, all of which `preact/compat`
provides (Preact ≥ 10.11), and it never touches `react-dom` or the JSX
runtime. `@preact/preset-vite` does the aliasing; nothing else is needed.

The phrase in your code is the lookup key **and** the base-language default —
no keys file, no extraction step.

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/langsys/langsys-demos/tree/main/preact)

## Run it

```bash
npm install
cp .env.example .env   # add a READ-ONLY Langsys key + project id
npm run dev
```

Then switch locale with the buttons and watch the page re-translate live.

## What's inside

- `vite.config.js` — `@preact/preset-vite`, which aliases `react` /
  `react-dom` → `preact/compat`. This file is the entire integration.
- `src/langsys.js` — creates the shared locale store and calls `LangsysApp.init()`.
- `src/App.jsx` — the demo: `useT()`, `<Translate>`, `<Phrase>` (with `%name%`
  markup params), and `<DontTranslate>` — identical to `../react/src/App.jsx`.

Without a key the app runs in demo mode (source text shows; the switcher still
works). A **read-only** key is safe to ship in a browser app.

## Learn more

- Interactive explorer: the Langsys Learning Center
- SDK: [`langsys-js-react`](https://github.com/langsys/langsys-js-react)
- API docs: [docs.langsys.dev](https://docs.langsys.dev)
