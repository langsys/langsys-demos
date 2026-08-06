# Langsys × Angular — starter

A minimal [Angular](https://angular.dev) 17+ app using
[`langsys-js-angular`](https://github.com/langsys/langsys-js-angular) for realtime,
continuous translations. The phrase in your code is the lookup key **and** the
base-language default — no keys file, no extraction step.

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/langsys/langsys-demos/tree/main/angular)

## Run it

```bash
npm install
cp .env.example .env   # optional — add a READ-ONLY Langsys key + project id
npm run dev
```

Then switch locale with the buttons and watch the page re-translate live.

## What's inside

- `src/langsys.ts` — creates the shared locale store and the `provideLangsys()` config.
- `src/main.ts` — `bootstrapApplication(AppComponent, { providers: [provideLangsys(...)] })`.
- `src/app.component.ts` — the demo: the `| t` pipe, `[lsTranslate]`, `[lsPhrase]`
  (with `%name%` markup params), and `[lsDontTranslate]`.

Without a key the app runs in demo mode (source text shows; the switcher still
works). A **read-only** key is safe to ship in a browser app.

## About the build

Angular is the one demo here that isn't a bare Vite app: it uses the Angular CLI
(`ng serve` / `ng build`, itself esbuild-powered), so `npm run dev`/`build` work
just like the siblings, and StackBlitz runs it natively. Env vars are read the
same `import.meta.env.VITE_*` way where available; under the Angular CLI, set your
project id/key in the `DEMO_*` constants in `src/langsys.ts` (or an Angular
`environment.ts`).

## Learn more

- Interactive explorer: the Langsys Learning Center
- SDK: [`langsys-js-angular`](https://github.com/langsys/langsys-js-angular)
- API docs: [docs.langsys.dev](https://docs.langsys.dev)
