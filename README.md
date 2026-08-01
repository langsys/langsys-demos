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
| Symfony (server-rendered) | [`langsys/symfony-sdk`](https://github.com/langsys/langsys-symfony) | [`./symfony`](./symfony) | [Codespaces](https://codespaces.new/langsys/langsys-demos?quickstart=1&devcontainer_path=.devcontainer%2Fsymfony%2Fdevcontainer.json) (StackBlitz can't run PHP) |
| NestJS (server-rendered) | [`langsys-js-nestjs`](https://github.com/langsys/langsys-js-nestjs) | [`./nestjs`](./nestjs) | run locally (installs the binding from the sibling repo until it's on npm) |
| Hono (server-rendered, edge-ready) | [`langsys-js-hono`](https://github.com/langsys/langsys-js-hono) | [`./hono`](./hono) | run locally (installs the binding from the sibling repo until it's on npm) |

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

The Symfony app is the same demo over the same PHP SDK, via the Symfony bundle:

```bash
cd symfony
composer install
php -S localhost:8000 -t public
```

The NestJS and Hono apps are the same demo translated by the Node server
bindings — multi-locale safe (one catalog per locale, so concurrent requests
in different locales never race). They install their binding from the sibling
`langsys-js-nestjs` / `langsys-js-hono` checkouts until those are on npm:

```bash
cd nestjs             # or hono
npm install
npm start             # nestjs → :3000, hono → :3001
```

Switch locale with the buttons and watch the page re-translate live. Each JS
app demonstrates the same surface — a shared locale store +
`LangsysApp.init()`, a locale switcher, and `t()` / `<Translate>` / `<Phrase>`
/ `<DontTranslate>`. The PHP apps demonstrate the backend surface — Laravel's
`@t` Blade directive and `t()` helper, Symfony's `t()` Twig function and
autowired translator, and each framework's locale detection; their locale
buttons are plain `?locale=` links the framework integration persists.

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
`src/langsys.js`/`.ts`, in the Laravel app's `config/langsys.php`, and in the
Symfony app's `src/Support/LangsysClientFactory.php` — all copies must match —
and the demo project's catalog must contain every phrase the apps render. After changing demo copy, run the app once with a write key so
the new phrases register and translate.

## Learn more

- Interactive explorers & side-by-side: the Langsys Learning Center
- API docs: [docs.langsys.dev](https://docs.langsys.dev)
