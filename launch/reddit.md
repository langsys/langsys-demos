# Reddit

One useful post per community, each written for that community, from a founder's personal account. Reddit punishes anything that reads like an ad: lead with the problem and the how, say plainly that you built it, and stay in the comments.

Before posting in each community, read its rules on the day: several allow self-promotion only on certain days or in a weekly thread, and some require a minimum account age or karma.

| Day | Community | Post |
|---|---|---|
| Launch + 2 · Wed 28 Oct 2026 | r/sveltejs | Svelte i18n without a keys file |
| Launch + 14 · Mon 9 Nov 2026 | r/SaaS | Adding German to a live store without a deploy |
| Launch + 35 · Mon 30 Nov 2026 | r/webdev | Plurals and gender agreement without branching in your code |
| Launch + 50 · Tue 15 Dec 2026 | r/reactjs | React i18n without a keys file (the day the React walkthrough goes public) |
| Launch + 91 · Mon 25 Jan 2027 | r/vuejs | Vue i18n without a keys file (the day the Vue walkthrough goes public) |

## Launch + 2 · Wed 28 Oct 2026 · r/sveltejs

**Title:**

```
I built a Svelte i18n library where the English sentence is the key (no keys file)
```

**Body:**

```
Every Svelte i18n setup I've used ends up with a JSON file of keys like `cart.empty.title` that drifts from the components. I wanted to write the sentence I mean and have the rest happen, so I built Langsys and its Svelte SDK.

What it looks like:

    <script>
      import { t } from 'langsys-js-svelte';
    </script>

    <h1>{$t('Your cart is empty', 'Cart')}</h1>

The first time that line runs, the phrase registers itself with Langsys and is machine-drafted in every language you've turned on; a translator can refine it later in a web app, and the fix reaches the running app without a redeploy.

Three Svelte-specific bits I'm happy with:

- `<Phrase>` keeps a sentence with markup inside as one phrase, so the translator sees the whole sentence and the bold lands where Spanish puts it.
- `<Translate>` wraps a whole region; every run of text inside registers itself, including placeholders, alt text and aria labels.
- `<DontTranslate>` keeps a brand name verbatim inside a sentence that still translates.

There's a one-minute walkthrough video here: https://youtu.be/y-YbRDjV4Wk
And a Svelte guide: https://docs.langsys.dev/learn?utm_source=reddit&utm_campaign=launch_2026&utm_content=r-sveltejs

The SDK is MIT on npm (`langsys-js-svelte`), works with SvelteKit (the catalog is seeded on the server so the first render is already translated), and the hosted service has a free plan.

I'd really like feedback from anyone running i18n in a large Svelte app: what would stop you from switching?
```

## Launch + 14 · Mon 9 Nov 2026 · r/SaaS

**Title:**

```
We added German to a live store in a few seconds, with no deploy. Here's how the pipeline we removed used to work.
```

**Body:**

```
Founder of Langsys here. I want to share the problem we built it around, because I think a lot of SaaS teams pay this tax without noticing.

Adding a language to an app usually means a project: extract every string into key files, send them to translators, wait, import them back, test, ship a release. Then every new sentence the team writes goes through the same loop, so the second language is always a few weeks behind the first.

We designed Langsys so that adding a language is a setting:

1. You turn on German in the project settings.
2. Langsys quotes the exact price for the existing catalog before anything runs (in our demo store: 29 words, $0.35).
3. AI drafts every phrase in seconds, and the live app switches to German. Nothing is built or deployed.
4. A person can then review and sharpen the drafts in the Translation Manager, and each fix is live immediately.

New phrases after that are drafted the moment the code first runs them, so the new language never falls behind.

The whole thing, in under two minutes: https://youtu.be/65z2J2jiSbY

Happy to answer questions about the pricing model (per source word, quoted up front), how we handle review, or what we got wrong on the way.
```

## Launch + 35 · Mon 30 Nov 2026 · r/webdev

**Title:**

```
Russian has 4 plural forms and Spanish greets Diego and Laura differently. How we handle both without an if in your code
```

**Body:**

```
Two i18n problems most apps get wrong outside English:

**Plurals.** English has two forms (1 file, 2 files). Russian has four: 1 файл, 2 файла, 5 файлов, and 21 файл goes back to the singular. Arabic has six. The usual answer is `count === 1 ? ... : ...`, which is wrong in most languages, or hand-writing an ICU plural message per language.

**Gender agreement.** In Spanish the greeting agrees with the person: ¡Bienvenido, Diego! / ¡Bienvenida, Laura! The usual answer is a conditional in the component, multiplied by every language that needs it.

In Langsys (I'm one of the people building it) you write the sentence once with a parameter, and the ICU branches each language needs are generated for that language: the four Russian plural forms, the Spanish gender forms, a neutral form when the gender is unknown. Your component never branches.

Short videos of both:
- Plurals: https://youtu.be/vkDmCusXKcI
- Gender: https://youtu.be/AfpNQtvugks

There's also a write-up of how ICU select and plural work under the hood in our docs: https://docs.langsys.dev/learn?utm_source=reddit&utm_campaign=launch_2026&utm_content=r-webdev

Curious how others handle this today, especially gender in languages with more than two agreement forms.
```

## Launch + 50 · Tue 15 Dec 2026 · r/reactjs

Posted the day the React walkthrough goes public. The link is the walkthrough's unlisted upload, so it works before that day too.

**Title:**

```
I built a React i18n library where the English sentence is the key (no keys file)
```

**Body:**

```
Every React i18n setup I've used ends up with a JSON file of keys like `cart.empty.title` that drifts from the components. I wanted to write the sentence I mean and have the rest happen, so I built Langsys and its React SDK.

What it looks like:

    import { useT } from 'langsys-js-react';

    function Cart() {
      const t = useT();
      return <h1>{t('Your cart is empty', 'Cart')}</h1>;
    }

The first time that line renders, the phrase registers itself with Langsys and is machine-drafted in every language you've turned on; a translator can refine it later in a web app, and the fix reaches the running app without a redeploy. Placeholders are type-checked: `t('Hello, {name}!', 'UI', {})` is a TypeScript error.

Three components I'm happy with:

- `<Phrase>` keeps a sentence with markup inside as one phrase, so the translator sees the whole sentence and the bold lands where Spanish puts it.
- `<Translate>` wraps a whole region; every run of text inside registers itself, including placeholders, alt text and aria labels.
- `<DontTranslate>` keeps a brand name verbatim inside a sentence that still translates.

One React-specific gotcha we had to design around: inside `<Phrase>` and `<Translate>` markup, placeholders are written `%count%`, because JSX evaluates `{count}` before the library ever sees the text. Debug mode warns if you get it wrong.

There's a one-minute walkthrough video here: https://youtu.be/sp4K9n4krZ4
And a React guide: https://docs.langsys.dev/learn/sdk/react?utm_source=reddit&utm_campaign=launch_2026&utm_content=r-reactjs

The SDK is MIT on npm (`langsys-js-react`), works with Next.js (seed the catalog on the server and the first render is already translated, with no flash on hydration), and the hosted service has a free plan.

I'd really like feedback from anyone running i18n in a large React app: what would stop you from switching?
```

## Launch + 91 · Mon 25 Jan 2027 · r/vuejs

Posted the day the Vue walkthrough goes public. The link is the walkthrough's unlisted upload, so it works before that day too.

**Title:**

```
I built a Vue i18n library where the English sentence is the key (no keys file)
```

**Body:**

```
Every Vue i18n setup I've used ends up with a JSON file of keys like `cart.empty.title` that drifts from the components. I wanted to write the sentence I mean and have the rest happen, so I built Langsys and its Vue SDK.

What it looks like:

    <script setup>
    import { useT } from 'langsys-js-vue';
    const t = useT();
    </script>

    <template>
      <h1>{{ t('Your cart is empty', 'Cart') }}</h1>
    </template>

The first time that line renders, the phrase registers itself with Langsys and is machine-drafted in every language you've turned on; a translator can refine it later in a web app, and the fix reaches the running app without a redeploy.

Three components I'm happy with:

- `<Phrase>` keeps a sentence with markup inside as one phrase, so the translator sees the whole sentence and the bold lands where Spanish puts it.
- `<Translate>` wraps a whole region; every run of text inside registers itself, including placeholders, alt text and aria labels.
- `<DontTranslate>` keeps a brand name verbatim inside a sentence that still translates.

One Vue-specific gotcha we had to design around: inside `<Phrase>` and `<Translate>`, write placeholders as `%name%`, not `{{ name }}`. Slot content is compiled by the parent template, so Vue substitutes `{{ name }}` before the library sees it. Debug mode warns if you get it wrong.

There's a one-minute walkthrough video here: https://youtu.be/1ROhtDzJWNo
And a Vue guide: https://docs.langsys.dev/learn/sdk/vue?utm_source=reddit&utm_campaign=launch_2026&utm_content=r-vuejs

The SDK is MIT on npm (`langsys-js-vue`), works with Nuxt (seed the catalog on the server so the first render is already translated), and the hosted service has a free plan.

I'd really like feedback from anyone running i18n in a large Vue app: what would stop you from switching?
```
