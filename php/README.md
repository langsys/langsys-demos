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

Switch locale with the links, or step the count, and the server renders the
page again. A first visit follows your browser's language.

To use your own project, set the credentials in the environment. A server can
hold a WRITE key — it never reaches visitors — and that's what lets new
phrases register themselves:

```bash
LANGSYS_PROJECT_ID=your-project-id LANGSYS_API_KEY=your-api-key php -S localhost:8000 -t public
```

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
