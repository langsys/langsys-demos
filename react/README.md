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

Then pick a language from the menu and watch the page re-translate live. The
menu lists the languages your project serves.

## Use your own project

The shared demo project is read-only, so its phrases are translated but one you
write stays in English: a read-only key can't register it. To watch the whole
loop, run the app on a project of your own:

1. At [app.langsys.dev](https://app.langsys.dev), create a project with English
   as the source, a few target languages, and **Automatically AI translate all
   new phrases** turned on.
2. Create a **Read & Write** key for it.
3. Do this in a **local clone**, never in a StackBlitz fork: forks are
   shareable, and a write key must stay private.

   ```bash
   cp .env.example .env
   ```

   Set `VITE_LANGSYS_PROJECT_ID` and `VITE_LANGSYS_API_KEY` (the write key).
4. `npm run dev`, then add a sentence of your own to `src/App.jsx` with `t('…', 'Greetings')`
   and reload. It registers, gets translated, and appears in every language you
   picked.

Translating your phrases uses your project's credits. The
[quickstart](https://docs.langsys.dev/learn/quickstart) walks through the same
steps, with a video.

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
