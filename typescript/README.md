# Langsys × TypeScript — starter

A minimal [Vite](https://vitejs.dev) + vanilla TypeScript app using
[`langsys-js-typescript`](https://github.com/langsys/langsys-js-typescript) —
the framework-agnostic base SDK every binding wraps — for realtime, continuous
translations. The phrase in your code is the lookup key **and** the
base-language default — no keys file, no extraction step. No framework: the
markup lives in `index.html` and the SDK drives the DOM directly.

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/langsys/langsys-demos/tree/main/typescript)

## Run it

```bash
npm install
cp .env.example .env   # add a READ-ONLY Langsys key + project id
npm run dev
```

Then switch locale with the buttons and watch the page re-translate live.

## What's inside

- `src/langsys.ts` — creates the shared locale `Signal` and calls `LangsysApp.init()`.
- `src/main.ts` — the demo: `t()` re-rendered via `tSignal`, the `Translate`
  and `Phrase` DOM classes (with `{count}` params — no framework template
  syntax to collide with), and the standard `translate="no"` attribute for
  the untouchables.
- `index.html` — the page. Every translatable sentence is written once, here.

Without a key the app runs in demo mode (source text shows; the switcher still
works). A **read-only** key is safe to ship in a browser app.

## Learn more

- Interactive explorer: the Langsys Learning Center
- SDK: [`langsys-js-typescript`](https://github.com/langsys/langsys-js-typescript)
- API docs: [docs.langsys.dev](https://docs.langsys.dev)
