# Langsys demos

The **same minimal app, built once per Langsys SDK** — showing realtime,
continuous translation across frameworks. Each subfolder is a standalone,
runnable Vite app; the phrase in the code is the lookup key *and* the
base-language default (no keys file, no extraction step).

| Framework | SDK | App | Open |
|-----------|-----|-----|------|
| React | [`langsys-js-react`](https://github.com/langsys/langsys-js-react) | [`./react`](./react) | [StackBlitz](https://stackblitz.com/github/langsys/langsys-demos/tree/main/react) |
| Svelte | [`langsys-js-svelte`](https://github.com/langsys/langsys-js-svelte) | [`./svelte`](./svelte) | [StackBlitz](https://stackblitz.com/github/langsys/langsys-demos/tree/main/svelte) |
| Vue | [`langsys-js-vue`](https://github.com/langsys/langsys-js-vue) | [`./vue`](./vue) | [StackBlitz](https://stackblitz.com/github/langsys/langsys-demos/tree/main/vue) |

## Run one

```bash
cd react              # or svelte, or vue
npm install
cp .env.example .env   # add a READ-ONLY Langsys key + project id
npm run dev
```

Switch locale with the buttons and watch the page re-translate live. Each app
demonstrates the same surface — a shared locale store + `LangsysApp.init()`, a
locale switcher, and `t()` / `<Translate>` / `<Phrase>` / `<DontTranslate>`.
Without a key each runs in demo mode (source text; the switcher still works). A
**read-only** key is safe to ship in a browser app.

## Learn more

- Interactive explorers & side-by-side: the Langsys Learning Center
- API docs: [docs.langsys.dev](https://docs.langsys.dev)
