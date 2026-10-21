---
title: "Russian has four plural forms. Your code shouldn't care."
published: false
description: "Why count === 1 is wrong in most languages, why gender agreement doesn't belong in your components, and how ICU plural and select solve both."
tags: i18n, javascript, webdev, localization
canonical_url: https://docs.langsys.dev/learn
---

<!-- dev.to front matter. For Hashnode, paste the body and set the same title, tags and canonical URL. Publish week 3 or 4. -->

Here's the plural logic in most apps:

```ts
const label = count === 1 ? `${count} file` : `${count} files`;
```

It's correct in English. It's wrong in most of the other languages your app will ever speak.

## How many plural forms does a language have?

English has two: *1 file*, *2 files*. Other languages don't stop there.

| Language | Forms | Example |
|---|---|---|
| English | 2 | 1 file, 2 files |
| French | 3 | 0 fichier, 2 fichiers, 1 000 000 de fichiers |
| Russian | 4 | 1 файл, 2 файла, 5 файлов, 21 файл |
| Arabic | 6 | zero, one, two, few, many, other |
| Japanese | 1 | no plural inflection at all |

Russian is the one that catches people: the form depends on the last digits, so *21 файл* goes back to the singular while *11 файлов* doesn't. No `count === 1` check gets that right, and writing the rules per language in your own code means maintaining CLDR by hand.

## ICU plural: the rules live in the translation

ICU MessageFormat moves the plural forms out of your code and into the message, where each language can have exactly the forms it needs:

```
{count, plural, one {# файл} few {# файла} many {# файлов} other {# файла}}
```

The runtime picks the right branch from the CLDR rules for the active locale. Your code passes a number and nothing else.

The catch is that someone has to write those branches, for every language, for every sentence with a count in it. In practice that someone is a developer who doesn't speak Russian.

## Write it flat; let the branches be generated

With Langsys you write the sentence once, flat, the way you'd say it in English:

```ts
t('You have {count} new messages', 'Inbox', { count });
```

Langsys generates the plural branches each language needs when it translates the phrase: four for Russian, six for Arabic, one for Japanese. The SDK renders the translation with full CLDR plural rules for the active locale. Your component never branches, and nobody types ICU by hand.

## Gender agreement: the same problem, one level up

Spanish agrees with the person:

- ¡Bienvenido, Diego!
- ¡Bienvenida, Laura!

And when the gender isn't known, a neutral form: *¡Te damos la bienvenida!*

The usual fix is a conditional in the component, multiplied by every language that needs one:

```ts
const greeting = user.gender === 'female' ? t('welcome_female') : t('welcome_male');
```

Now there are two keys, the English for both is the same sentence, and a third case (unknown) needs a third key. ICU `select` handles this the same way `plural` handles counts:

```
{name_gender, select, male {¡Bienvenido, {name}!} female {¡Bienvenida, {name}!} other {¡Te damos la bienvenida, {name}!}}
```

In Langsys, again, you write one flat sentence and pass the value:

```ts
t('Welcome, {name}!', 'Onboarding', { name: user.name, name_gender: user.gender });
```

`name_gender` is the gender of whoever `{name}` refers to. The select branches are generated only for the languages that agree with the person: the Spanish catalog grows `{name_gender, select, …}`, while English and French stay one sentence. If the value is missing, the neutral `other` branch is used. Diego, Laura and someone with no gender on record are each greeted correctly, from one line.

## The rule of thumb

If your component contains a branch whose only job is grammar (`count === 1`, `gender === 'female'`), that branch belongs in the translation, not in your code. ICU is the format for it; generating the branches is what makes it practical.

## Watch it

- Plurals, in 14 seconds: https://youtu.be/vkDmCusXKcI
- Plurals in every language, the full video: https://youtu.be/vwQknki_V6A
- Gender agreement with ICU select: https://youtu.be/AfpNQtvugks
- Docs: https://docs.langsys.dev/learn

The SDKs are MIT on npm and Packagist, and there's a free plan if you want to see your own app's sentences come back in Russian.
