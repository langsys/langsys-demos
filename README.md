# Langsys demos

The **same minimal app, built once per Langsys SDK** — showing realtime,
continuous translation across stacks. Each subfolder is standalone and
runnable; the phrase in the code is the lookup key *and* the base-language
default (no keys file, no extraction step).

| Stack | SDK | App | Open |
|-------|-----|-----|------|
| TypeScript (vanilla) | [`langsys-js-typescript`](https://github.com/langsys/langsys-js-typescript) | [`./typescript`](./typescript) | [StackBlitz](https://stackblitz.com/github/langsys/langsys-demos/tree/main/typescript) |
| React | [`langsys-js-react`](https://github.com/langsys/langsys-js-react) | [`./react`](./react) | [StackBlitz](https://stackblitz.com/github/langsys/langsys-demos/tree/main/react) |
| Preact (via `preact/compat`) | [`langsys-js-react`](https://github.com/langsys/langsys-js-react) — unchanged | [`./preact`](./preact) | [StackBlitz](https://stackblitz.com/github/langsys/langsys-demos/tree/main/preact) |
| Svelte | [`langsys-js-svelte`](https://github.com/langsys/langsys-js-svelte) | [`./svelte`](./svelte) | [StackBlitz](https://stackblitz.com/github/langsys/langsys-demos/tree/main/svelte) |
| Vue | [`langsys-js-vue`](https://github.com/langsys/langsys-js-vue) | [`./vue`](./vue) | [StackBlitz](https://stackblitz.com/github/langsys/langsys-demos/tree/main/vue) |
| Laravel (server-rendered) | [`langsys/laravel-sdk`](https://github.com/langsys/langsys-laravel) | [`./laravel`](./laravel) | [Codespaces](https://codespaces.new/langsys/langsys-demos?quickstart=1&devcontainer_path=.devcontainer%2Flaravel%2Fdevcontainer.json) (StackBlitz can't run PHP) |

## Run one

The JS apps are Vite apps:

```bash
cd react              # or svelte, vue, or typescript (vanilla, no framework)
npm install
npm run dev           # runs on the shared demo project by default
```

The Laravel app translates on the server (PHP 8.2+ and Composer required —
StackBlitz only runs Node, so its browser sandbox is a
[Codespace](https://codespaces.new/langsys/langsys-demos?quickstart=1&devcontainer_path=.devcontainer%2Flaravel%2Fdevcontainer.json)
instead):

```bash
cd laravel
composer install
cp .env.example .env && php artisan key:generate
php artisan serve
```

Switch locale with the buttons and watch the page re-translate live. Each JS
app demonstrates the same surface — a shared locale store +
`LangsysApp.init()`, a locale switcher, and `t()` / `<Translate>` / `<Phrase>`
/ `<DontTranslate>`. The Laravel app demonstrates the backend surface — the
`@t` Blade directive, the `t()` helper, and the locale-detection middleware;
its locale buttons are plain `?locale=` links the middleware persists.

Each app is the live version of its SDK's Learning Center page
([docs.langsys.dev/learn/sdk/…](https://docs.langsys.dev/learn/sdk/typescript)):
every example the docs page shows runs in the app, wired by the same code.

By default the apps run on the **shared demo project** — a public read-only key
over a fixed, pre-translated catalog (a banner in the app says so). Existing
phrases translate; new or edited ones won't, because read-only keys can't
register tokens. To watch discovery register and translate *your* phrases,
`cp .env.example .env` in a **local clone** and use your project id with a
**write** key — never paste a write key into a StackBlitz sandbox (forks are
shareable; read-only keys are the only kind safe to publish).

Maintainers: the shared demo credentials live in each JS app's
`src/langsys.js`/`.ts` and in the Laravel app's `config/langsys.php` — all five
copies must match — and the demo project's catalog must contain every phrase
the apps render. After changing demo copy, run the app once with a write key so
the new phrases register and translate.

## Learn more

- Interactive explorers & side-by-side: the Langsys Learning Center
- API docs: [docs.langsys.dev](https://docs.langsys.dev)
