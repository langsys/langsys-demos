# X posts for the YouTube calendar

One post per video, on the day it goes public (`python upload.py --publish`). Dates follow `publish` in `../youtube/videos.json`; if the calendar moves with `--reschedule`, regenerate the dates. Each post is under 280 characters, counting the link as 23 the way X does. The link is the youtu.be address, which works once the video is public.

## Monday 2026-10-19

**What is Langsys? Your app in every language, no redeploy** · 213 characters

```
Your app, in every language. No keys file, no extraction step, no redeploy.

A blog post published at 09:00 reaches a reader in Madrid, in Spanish, at 09:03.

Here's Langsys in 77 seconds 👇
https://youtu.be/_DFWgHZ_QQc
```

**Getting started with Langsys, end to end** · 179 characters

```
From an empty project to an app that switches to Spanish and French without a reload, in one take.

No .json files were harmed in the making of this video.
https://youtu.be/Fo1HCybAHg0
```

**Plurals in every language, without if (count === 1)** · 207 characters

```
if (count === 1) is English grammar living in your code.

Russian has four plural forms. Arabic has six. Write the sentence flat once and Langsys builds every form for every language.
https://youtu.be/vwQknki_V6A
```

## Wednesday 2026-10-21

**The translation pipeline, and how Langsys deletes it** · 139 characters

```
Extract → export → translate → import → deploy.

Every i18n setup has this pipeline. We deleted it.

Concepts 1/5 👇
https://youtu.be/DDBgZpPxn_k
```

## Friday 2026-10-23

**No more key files: the sentence is the key** · 182 characters

```
checkout.button.submit.label

Somebody had to invent that key, and somebody has to keep it in sync forever.

In Langsys the sentence is the key. Concepts 2/5:
https://youtu.be/8ityN0zlu98
```

**Your i18n key is just the English sentence #Shorts** · 91 characters

```
Your i18n key is just… the English sentence.

In under 15 seconds 👇
https://youtu.be/L4uu_oG9uok
```

## Monday 2026-10-26

**The locale store: holding and switching the active language** · 123 characters

```
One store holds the active language. Switch it and the whole app follows, no reload.

Concepts 3/5:
https://youtu.be/E6qqpBC_7IY
```

**Russian has 4 plural forms. You write one line #Shorts** · 157 characters

```
1 файл. 2 файла. 5 файлов. 21 файл.

Russian picks a plural form by the number, and 21 goes back to the singular. You write one line.
https://youtu.be/vkDmCusXKcI
```

## Wednesday 2026-10-28

**API keys and environments: which key goes where** · 174 characters

```
A key that can register phrases can't ship. A read-only key is a dead end.

So we made a key whose answer depends on where you ask from. Concepts 4/5:
https://youtu.be/dfaCUjRA168
```

## Friday 2026-10-30

**Adding a new language is a project setting** · 169 characters

```
Reaching a new market shouldn't be a project. It should be a setting.

New phrases translate on arrival; one run fills in the rest. Concepts 5/5:
https://youtu.be/9muq4sNC_Zg
```

## Monday 2026-11-02

**Svelte i18n with Langsys: the full walkthrough** · 193 characters

```
Svelte devs: here's i18n with nothing to keep in step.

One call, a locale switch, and why flat Spanish is wrong for half your users (and what ICU select does about it).
https://youtu.be/y-YbRDjV4Wk
```

## Wednesday 2026-11-04

**t(phrase, category, params) in Svelte** · 118 characters

```
t(phrase, category, params)

Three arguments. No keys file. Placeholders and plurals included.
https://youtu.be/mqFBw6x7RZg
```

## Friday 2026-11-06

**‹Phrase› in Svelte: a sentence with markup inside** · 165 characters

```
"Read the <a>terms</a> before you <b>sign</b>."

One sentence, markup inside, still one phrase for the translator. Here's <Phrase> in Svelte:
https://youtu.be/r85P18fhfCU
```

## Monday 2026-11-09

**‹Translate› in Svelte: one tag for a whole region** · 140 characters

```
Wrap a region in one <Translate> tag and every line inside registers itself.

Why a block beats a t() call per line:
https://youtu.be/krgkcNYw4IY
```

## Wednesday 2026-11-11

**‹DontTranslate› in Svelte: keep brand names verbatim** · 175 characters

```
Nobody wants their brand name translated into Spanish.

<DontTranslate> keeps names and identifiers verbatim, without pulling them out of the sentence.
https://youtu.be/YPyWNGdaAHw
```

## Friday 2026-11-13

**What is a content block? Translating a whole section in Svelte** · 162 characters

```
What is a content block?

A whole section registered as one unit, so it's translated with its context, and still made of reusable phrases.
https://youtu.be/-ZMV0UyKRVk
```

**Translate a whole section with one tag #Shorts** · 128 characters

```
Translate a whole section with one tag. Bold and links land where they belong; the brand name stays put.
https://youtu.be/zw9iKNfjVng
```

## Monday 2026-11-16

**Same word, two meanings: categories instead of i18n keys** · 147 characters

```
"Book" a flight or read a "book"?

Same word, two meanings. This is why i18n invented keys. Categories fix it without them:
https://youtu.be/-P963Wj0dno
```

## Wednesday 2026-11-18

**Gender agreement without conditionals in your code (ICU select)** · 182 characters

```
{gender === 'f' ? 'Bienvenida' : 'Bienvenido'}

That conditional doesn't belong in your component. Langsys generates the gender branches per language instead.
https://youtu.be/AfpNQtvugks
```

**Bienvenido or Bienvenida? One line of code #Shorts** · 112 characters

```
Bienvenido or Bienvenida?

Diego, Laura and an unknown user, all from one line of code 👇
https://youtu.be/6bMkgdK1GpU
```

## Friday 2026-11-20

**Translating placeholders, alt text and aria labels in Svelte** · 166 characters

```
A form with a translated label and an English placeholder is a half-translated form.

Placeholders, alt text and aria labels in the same pass:
https://youtu.be/w9TNoFQ2fpM
```

## Monday 2026-11-23

**Numbers and dates in every locale with Svelte i18n** · 162 characters

```
1,234.5 in the US. 1.234,5 in Germany. 12,34,567 in India.

Digit grouping is a shape, not a separator. Numbers and dates in every locale:
https://youtu.be/Bc2h2bxaB9M
```

## Wednesday 2026-11-25

**Translation memory: a new project that starts already translated** · 189 characters

```
We opened a brand new project. It was already fully translated.

Translation memory carries every sentence, and who wrote it, across your projects. Zero model calls.
https://youtu.be/QC2IIRaAyCc
```

## Friday 2026-11-27

**Use Langsys from Claude Code over MCP** · 147 characters

```
Ask Claude Code "which languages are behind in my project?" and get the answer from live data.

One claude mcp add command:
https://youtu.be/KafvNJnm-pQ
```

## Monday 2026-11-30

**Add German to a live app: exact quote, no deploy** · 156 characters

```
Adding German to a live store: exact quote before anything runs (29 words, $0.35), then it's live.

Nothing built, nothing deployed.
https://youtu.be/65z2J2jiSbY
```

## Wednesday 2026-12-02

**Catching up a language that fell behind** · 141 characters

```
A language fell behind? One click, a confirmation with the exact cost per locale, and every language is back to 100%.
https://youtu.be/SHHt8ebaH-g
```

## Friday 2026-12-04

**AI Translator settings, every switch explained** · 154 characters

```
Every switch in the AI Translator, explained. Including the one that spots a phrase that's already in Spanish and leaves it alone.
https://youtu.be/PnRoVVfYmKE
```

## Monday 2026-12-07

**API keys in production: activity, pausing and rotation** · 161 characters

```
A week of real storefront traffic on a key's activity page, a pause without deleting, and a live key rotation.

API keys after they ship:
https://youtu.be/jZJRja7n_-c
```

## Wednesday 2026-12-09

**One organization, many projects** · 145 characters

```
Agencies, this one's for you: one organization, many projects, settings inherited by default and overridden where needed.
https://youtu.be/y1kGQkoZ3_w
```

## Friday 2026-12-11

**Usage and credits: how a project gets funded** · 138 characters

```
How a project gets funded: API usage, credits, one line per machine translation in its history, and auto recharge.
https://youtu.be/TOqn3rfDyGQ
```

## Monday 2026-12-14

**Plans and payments in Langsys** · 142 characters

```
Plans, billing cycle, payment methods shared across an organization, invoices.

The boring part, in under two minutes:
https://youtu.be/3Lnmfo0T71Q
```

## Wednesday 2026-12-16

**Notifications: what Langsys tells you, and where** · 128 characters

```
New phrases, invitations, project access: what Langsys tells you, where, and how to tune it per project.
https://youtu.be/gpSYSKrmVp0
```
