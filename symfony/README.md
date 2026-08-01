# Langsys × Symfony demo

Every example on [docs.langsys.dev/learn/sdk/symfony](https://docs.langsys.dev/learn/sdk/symfony)
running live, wired by the exact code the docs page shows. Translation happens
on the server — view source: the HTML arrives already localized.

```bash
composer install
php -S localhost:8000 -t public
```

Then open <http://localhost:8000>. Switch locale with the pills — they're plain
`?locale=` links the bundle's `LocaleSubscriber` resolves and persists (cookie).

By default the app runs on the **shared demo project** — a public read-only key
over a fixed, pre-translated catalog (the banner says so). To watch discovery
register and translate *your* phrases, put your project id and a **write** key
in `.env.local`:

```bash
LANGSYS_API_KEY=your-write-key
LANGSYS_PROJECT_ID=your-project-id
```

What's demonstrated (each card maps to a section of the docs page):

- `t()` in Twig — inline phrase + `{name}` params
- ICU plurals, resolved server-side per locale
- The autowired `LangsysTranslator` in a controller
- Categories disambiguating identical phrases
- Explicit coverage — untagged text passes through verbatim

The demo-only parts a real app wouldn't have: the `langsys.client` override in
`config/services.yaml` (shared-project fallback + offline stand-in) — delete it
and just set the two env vars.
