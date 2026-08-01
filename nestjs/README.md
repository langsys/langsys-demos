# Langsys × NestJS demo

The shared demo app, server-rendered by [`langsys-js-nestjs`](https://github.com/langsys/langsys-js-nestjs) — the same phrases and categories as the Laravel and Symfony demos, translated on the server. View source: the HTML arrives already localized.

```bash
npm install
npm start          # http://localhost:3000
```

Runs on the shared read-only demo project by default (existing phrases translate; new ones won't). Copy `.env.example` → `.env` and add your own keys to watch token discovery register phrases live.

The locale switcher is plain links — `LangsysLocaleMiddleware` picks up `?locale=`, persists it in a cookie, and loads that locale's catalog per request. Concurrent requests in different locales are safe: the binding keeps one catalog per locale.
