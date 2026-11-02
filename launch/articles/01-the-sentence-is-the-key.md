---
title: "Delete your i18n keys file: the sentence is the key"
published: false
description: "Why most i18n libraries make you invent a name for every sentence, what that costs, and what an app looks like when the sentence itself is the key."
tags: i18n, javascript, webdev, localization
canonical_url: https://docs.langsys.dev/learn
---

<!-- dev.to front matter. For Hashnode, paste the body and set the same title, tags and canonical URL. Publish week 2 (launch + 7 to + 11). -->

Every project starts with one app, one language and one sentence:

```html
<h1>Welcome to my app</h1>
```

Then you add a second language, and most i18n libraries ask you to do something that has nothing to do with translation: invent a name for that sentence.

```ts
t('home.hero.welcome_title')
```

```json
// en.json
{ "home": { "hero": { "welcome_title": "Welcome to my app" } } }

// es.json
{ "home": { "hero": { "welcome_title": "Bienvenido a mi app" } } }
```

## What the key costs you

The key looks harmless. It isn't free.

- **The sentence leaves your code.** Reading a component, you see `home.hero.welcome_title`, not what the user reads. Reviewing copy means opening a JSON file next to every component.
- **Every language is another file to keep in step.** Nine languages is nine files, and each one drifts on its own. A key added to `en.json` and forgotten in `fr.json` doesn't fail the build; it ships, and a French user sees `home.hero.welcome_title` on the screen.
- **Someone has to name things.** `welcome_title`, `welcomeTitle`, `hero.title`, `title_welcome`: teams spend real review time on names nobody outside the team ever sees.
- **The pipeline grows around it.** Extract the keys, export the files, send them to translators, import them back, ship a release. Change one word of English copy and the whole loop runs again.

None of that is translation. It's bookkeeping.

## The sentence is already a perfectly good key

The sentence you wrote is unique enough, readable, and it's exactly what the translator needs to see. So use it:

```ts
import { t } from 'langsys-js-typescript';

t('Welcome to my app', 'Home');
```

That one line is the lookup key *and* the source-language text. There's no `en.json`, because the English is in the code. There's no `es.json` either: translations live in Langsys, and the SDK loads the active language's catalog at runtime.

The first time that line runs, the SDK registers the phrase with Langsys. From there, depending on how the project is set up, it's machine-translated into every language you've turned on, or it waits for a translator. Either way a person can review it in the Translation Manager, and the correction reaches the running app without a build or a deploy.

## "But the same word means two things"

That's the one real job a key used to do: telling apart two identical English strings that translate differently. "Free" as a price is *gratis* in Spanish; "Free" as an empty evening is *libre*.

You don't need an invented name for that, just a category:

```ts
t('Free', 'Pricing');   // gratis
t('Free', 'Calendar');  // libre
```

The translator sees which one they're translating, and the code still reads like the screen. Use a category when a phrase genuinely means different things in different parts of the app; otherwise translate it once and use it everywhere.

## Placeholders, not string building

Dynamic values go in as parameters, never concatenated into the sentence:

```ts
t('Hello, {name}!', 'Greetings', { name });     // right
t(`Hello, ${name}!`, 'Greetings');              // wrong: registers a new phrase per user
```

In TypeScript the placeholder names are checked at compile time, so a missing or misspelled parameter is an error at the call site. Numbers and dates passed as parameters are formatted for the active locale (`1234.5` becomes `1.234,5` in German); pass an order number as a string and it stays exactly as written.

## What changes day to day

- A developer writes the copy in the component and moves on. Nothing to name, nothing to add to nine files.
- A translator sees every phrase beside its translations and fixes the ones that need it, live.
- A product manager changes a word and it's showing, instead of waiting on a release.

## Try it

The SDKs are open source (MIT): `langsys-js-typescript`, `langsys-js-react`, `langsys-js-vue` and `langsys-js-svelte` on npm, and `langsys/langsys-php` (with Laravel and Symfony bindings) on Packagist. There's a free plan to try it on a real project.

- The key-file problem, in 40 seconds: https://youtu.be/8ityN0zlu98
- Getting started, end to end: https://youtu.be/Fo1HCybAHg0
- Docs and the Learning Center: https://docs.langsys.dev/learn?utm_source=devto&utm_campaign=launch_2026&utm_content=the-sentence-is-the-key

If you maintain a keys file in a large app, I'd like to hear where you think this approach would break for you.
