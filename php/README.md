# Langsys × PHP — starter

A minimal plain-PHP page using
[`langsys/langsys-php`](https://github.com/langsys/langsys-php), no framework.
The live version of the [PHP page](https://docs.langsys.dev/learn/sdk/php).
Translation happens on the server, so the HTML arrives already localized.

## Run it

PHP 8.1+ with the `intl` and `curl` extensions, and Composer.

```bash
composer install
php -S localhost:8000 -t public     # on the shared demo project
```

Pick a language from the menu (the ones the project serves), or step the
count, and the server renders the page again. A first visit follows your browser's language.

To use your own project, set the credentials in the environment. A server can
hold a WRITE key — it never reaches visitors — and that's what lets new
phrases register themselves:

```bash
LANGSYS_PROJECT_ID=your-project-id LANGSYS_API_KEY=your-api-key php -S localhost:8000 -t public
```

## Use your own project

The shared demo project is read-only, so its phrases are translated but one you
write stays in English: a read-only key can't register it. To watch the whole
loop, run the app on a project of your own:

1. At [app.langsys.dev](https://app.langsys.dev), create a project with English
   as the source, a few target languages, and **Automatically AI translate all
   new phrases** turned on.
2. Create a **Read & Write** key for it.
3. Run the page with your project's id and the write key. A server can hold a
   write key; it never reaches visitors:

   ```bash
   LANGSYS_PROJECT_ID=your-project-id LANGSYS_API_KEY=your-write-key php -S localhost:8000 -t public
   ```
4. Add a sentence of your own to `public/index.php` with
   `<?= t('…', 'Greetings') ?>` and load the page. It's registered after the
   response, translated, and shows in every language you picked from the next
   load on.

Translating your phrases uses your project's credits. The
[quickstart](https://docs.langsys.dev/learn/quickstart) walks through the same
steps, with a video.

## What's inside

- `helpers.php` — one `Client` per request, the visitor's locale (`?locale=`,
  then a cookie, then `Accept-Language`), and the `t()` helper from the docs.
- `public/index.php` — the demo: `t()` in a template, a plural written flat,
  `translate()` outside a template with a locale-formatted date, categories,
  and untagged text that never translates.

## Learn more

- Docs: [docs.langsys.dev/learn/sdk/php](https://docs.langsys.dev/learn/sdk/php)
- SDK: [`langsys/langsys-php`](https://github.com/langsys/langsys-php)
- On Laravel? See [`../laravel`](../laravel).
