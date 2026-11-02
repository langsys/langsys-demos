# Langsys × Laravel — starter

A minimal [Laravel 12](https://laravel.com) app using
[`langsys/langsys-php-laravel`](https://github.com/langsys/langsys-php-laravel) for
realtime, continuous translations — server-rendered, so the page arrives
already localized (view source!). The phrase in your code is the lookup key
**and** the base-language default — no keys file, no extraction step.

No StackBlitz link for this one: WebContainers only run Node, not PHP. Run it
locally (PHP 8.2+ and Composer), or one-click a real PHP container instead:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/langsys/langsys-demos?quickstart=1&devcontainer_path=.devcontainer%2Flaravel%2Fdevcontainer.json)

The Codespace installs dependencies and starts `php artisan serve` on port
8000 automatically (see `.devcontainer/laravel/` at the repo root). It runs
without credentials — demo mode — unless you add your own in `laravel/.env`.

## Run it locally

```bash
composer install
cp .env.example .env
php artisan key:generate
php artisan serve       # http://127.0.0.1:8000
```

No database needed — sessions and cache run on the `file` drivers.

Then pick a language from the menu (a plain `?locale=` form — the
`DetectLocale` middleware persists your choice) and watch the page come back
re-translated. The menu lists the languages your project serves.

## Use your own project

The shared demo project is read-only, so its phrases are translated but one you
write stays in English: a read-only key can't register it. To watch the whole
loop, run the app on a project of your own:

1. At [app.langsys.dev](https://app.langsys.dev), create a project with English
   as the source, a few target languages, and **Automatically AI translate all
   new phrases** turned on.
2. Create a **Read & Write** key for it.
3. In `.env`, set `LANGSYS_PROJECT_ID` and `LANGSYS_API_KEY` (the write key). A
   server can hold a write key; it never reaches visitors.
4. Add a sentence of your own to `resources/views/demo.blade.php` with
   `@t('…', 'Greetings')` and load the page. It's registered after the
   response, translated, and shows in every language you picked from the next
   load on.

Translating your phrases uses your project's credits. The
[quickstart](https://docs.langsys.dev/learn/quickstart) walks through the same
steps, with a video.

## What's inside

- `bootstrap/app.php` — appends the two SDK middleware: `DetectLocale`
  (locale from query/cookie/session/`Accept-Language`) and
  `FlushPendingRegistrations` (registers newly rendered phrases *after* the
  response is sent).
- `routes/web.php` — the single route; shows `t()` working outside Blade,
  with locale-formatted date params.
- `resources/views/demo.blade.php` — the demo: `@t` inline strings, ICU
  plurals, category disambiguation, and the explicit-coverage contrast
  (untagged text passes through verbatim — no opt-out marker needed).
- `config/langsys.php` — the published SDK config, with the shared demo
  project as a read-only fallback.

Without a key the app runs in demo mode (source text shows; the switcher
still works). Unlike the browser demos, a **write** key is fine here — it
stays on the server and is never shipped to visitors; it's what lets brand-new
phrases register themselves in your dashboard.

## Learn more

- Interactive explorer: the Langsys Learning Center —
  [docs.langsys.dev/learn/sdk/laravel](https://docs.langsys.dev/learn/sdk/laravel)
- SDK: [`langsys/langsys-php-laravel`](https://github.com/langsys/langsys-php-laravel)
  (wraps [`langsys/langsys-php`](https://github.com/langsys/langsys-php))
- API docs: [docs.langsys.dev](https://docs.langsys.dev)
