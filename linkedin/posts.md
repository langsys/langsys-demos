# LinkedIn posts for the publishing calendar

One post per publishing day, on the same days as `x/posts.md`, from the Langsys company page. Nothing here goes out before the official launch.

- **Video goes up on LinkedIn itself.** LinkedIn shows posts with outside links to fewer people, so the post carries the video and the YouTube link goes in the first comment.
- **Shorts** go up as their silent 1:1 cut (it has no sound, so the on-screen text carries it). **Long videos** go up as the same captioned clip as on X.
- **Written for the people who own the product and the copy**, not only developers: what a team stops doing, what it costs, who does the work. The first two lines are all that shows before "see more", so they carry the hook.
- Three hashtags at the end, no more. Days are counted from launch Monday ("launch + N").
- A post marked **On hold** goes out only once its video is public.

## Week 1, Monday (launch day)

**Launch post** · upload the full 77-second explainer (`videos/explainer.mp4`)

```
Your app, in every language. No keys file, no extraction step, no redeploy.

Today we're launching Langsys.

Most teams translate their app the same way: extract the strings, export a file, wait for translators, import it back, ship a release. Every new sentence starts the loop again.

With Langsys, a phrase registers itself the first time your code runs it, is drafted by AI the moment it arrives, and can be reviewed and refined by a person in the Translation Manager. The fix is live in the app with nothing deployed.

A blog post published at 09:00 reaches a reader in Madrid, in Spanish, at 09:03.

The whole starting path is on YouTube today: getting started, plurals, the five concepts, and connecting your AI assistant. Links in the first comment.

#Localization #i18n #SaaS
```

First comment:

```
What is Langsys, in 77 seconds: https://youtu.be/_DFWgHZ_QQc
Getting started, end to end: https://youtu.be/Fo1HCybAHg0
Every video, in order, in the Learning Center: https://docs.langsys.dev/learn
```

## Week 1, Tuesday (launch + 1)

**Short: Your i18n key is just the English sentence**

```
Your translation key is the English sentence.

No keys file to invent, no strings to extract, nothing to keep in sync between your code and your translations.

Developers write the sentence they mean. Translators see the sentence they need to translate. Nobody maintains a list of names like checkout.cart.empty_state.title in between.

#i18n #Localization #WebDev
```

Upload `videos/svelte/social/phrase-1x1.mp4`.

First comment: `https://youtu.be/L4uu_oG9uok`

## Week 1, Wednesday (launch + 2)

**Video: Svelte i18n with Langsys: the full walkthrough**

```
For Svelte teams: your app in every language, with nothing to keep in step.

The full walkthrough, from the first translated line to a live language switch, including why one flat Spanish translation is wrong for half your users, and how Langsys fixes it without a branch in your code.

Full video in the first comment.

#Svelte #i18n #WebDev
```

Upload `videos/x/svelte/hero.mp4`.

First comment: `https://youtu.be/y-YbRDjV4Wk`

## Week 1, Thursday (launch + 3)

**Short: Russian has 4 plural forms. You write one line**

```
1 файл. 2 файла. 5 файлов. 21 файл.

Russian picks a plural form by the number, and 21 goes back to the singular. Arabic has six forms.

Most apps get this wrong in every language but English, because someone has to write each form by hand. With Langsys you write the sentence once, and every form each language needs is built for you.

#i18n #Localization #WebDev
```

Upload `videos/svelte/social/icu-plurals-1x1.mp4`.

First comment: `https://youtu.be/vkDmCusXKcI`

## Week 1, Friday (launch + 4)

**Video: Managing translations in the Langsys Translation Manager**

```
Every phrase your app has ever shown, in one place, where a person can review it and sharpen the wording.

A tour of the Langsys Translation Manager, for whoever owns the copy. No code on screen: the to-do list, an AI draft corrected by hand, a translator invited to Spanish only.

The correction is live in the app the moment it's saved. Nobody files a ticket, and nothing is deployed.

#Localization #Translation #SaaS
```

Upload `videos/x/managing-translations.mp4`.

First comment: `https://youtu.be/6ef3Mc0ILfk`

> On hold: Filmed against translation-manager MR !1; until it ships, Send on the invite dialog errors on the live app. Post only once the video is public.

## Week 2, Monday (launch + 7)

**Video: t(phrase, category, params) in Svelte**

```
One call, every language.

t(phrase, category, params) replaces the keys file: placeholders and plurals included, and the sentence in your code is the one your translators see.

Full video in the first comment.

#Svelte #i18n #WebDev
```

Upload `videos/x/svelte/t-string.mp4`.

First comment: `https://youtu.be/mqFBw6x7RZg`

## Week 2, Tuesday (launch + 8)

**Short: Published at 09:00, read in Spanish at 09:03**

```
Published at 09:00. Read in Spanish at 09:03.

No build, no deploy, and no developer involved.

A blog post goes live. The first time a reader opens it, Langsys reads the page, translates it, and a reader in Madrid gets it in Spanish minutes later. Content teams publish on their own schedule, in every language.

#Localization #ContentMarketing #SaaS
```

Upload `videos/shared/social/published-at-nine-1x1.mp4`.

First comment: `https://youtu.be/2pSiq0Xe4mI`

## Week 2, Wednesday (launch + 9)

**Video: Translation memory: a new project that starts already translated**

```
We opened a brand-new project. It was already translated.

Translation memory carries every sentence, and who wrote it, across every project in your organization. The second project starts out knowing what the first one learned, so no AI model is called and nothing is paid for twice.

Full video in the first comment.

#Localization #Translation #SaaS
```

Upload `videos/x/translation-memory.mp4`.

First comment: `https://youtu.be/QC2IIRaAyCc`

## Week 2, Thursday (launch + 10)

**Short: Ask your AI assistant how your translations are doing**

```
Ask your AI assistant how your translations are doing. Then ask it to translate what's missing.

Langsys hosts an MCP server, so Claude, Codex, Cursor or GitHub Copilot can read your projects and do the work. You approve it once in your browser, and the assistant never sees your password.

#AI #MCP #Localization
```

Upload `videos/shared/social/ask-your-assistant-1x1.mp4`.

First comment: `https://youtu.be/6AkTyjzK5_c`

## Week 2, Friday (launch + 11)

**Video: ‹Phrase› in Svelte: a sentence with markup inside**

```
A sentence with a bold word in it is still one sentence.

Most i18n tools cut it into three fragments, and the translator never sees the whole thing. With ‹Phrase›, the translator reads it whole, and the bold lands wherever each language puts it.

Full video in the first comment.

#Svelte #i18n #WebDev
```

Upload `videos/x/svelte/phrase-tag.mp4`.

First comment: `https://youtu.be/r85P18fhfCU`

## Week 3, Monday (launch + 14)

**Video: Add German to a live app: exact quote, no deploy**

```
Adding German to a live store: an exact price before anything runs, every phrase drafted in seconds, and the store speaks German.

Nothing built. Nothing deployed.

Opening a new market is a setting, not a project: Langsys quotes the existing catalog to the cent (29 words, $0.35 in this demo), translates it, and the live store switches.

#Localization #Ecommerce #SaaS
```

Upload `videos/x/adding-a-language.mp4`.

First comment: `https://youtu.be/65z2J2jiSbY`

## Week 3, Tuesday (launch + 15)

**Short: A brand-new project that starts already translated**

```
A brand-new project, already in Spanish.

Someone fixed one word in another project. This one already knew.

Fix a translation once, and every new project in your organization starts with it, credited to the translator who made it.

#Localization #Translation #SaaS
```

Upload `videos/shared/social/memory-1x1.mp4`.

First comment: `https://youtu.be/daw8QZbaaM4`

## Week 3, Wednesday (launch + 16)

**Video: ‹Translate› in Svelte: one tag for a whole region**

```
Wrap a whole region in one ‹Translate› tag, and every line inside registers itself.

No call per line, and nothing for a developer to forget when the copy changes.

Full video in the first comment.

#Svelte #i18n #WebDev
```

Upload `videos/x/svelte/translate-tag.mp4`.

First comment: `https://youtu.be/krgkcNYw4IY`

## Week 3, Thursday (launch + 17)

**Short: In Spanish, the bold moves to where it belongs**

```
In Spanish, the bold moves to where Spanish puts it.

"Unread messages" becomes "mensajes no leídos", and the emphasis has to follow the meaning, not the English word order.

Your translator gets one sentence, markup and all, and puts the bold where it belongs.

#Localization #i18n #WebDev
```

Upload `videos/svelte/social/bold-moves-1x1.mp4`.

First comment: `https://youtu.be/OtSqBQkO6TU`

## Week 3, Friday (launch + 18)

**Video: Catching up a language that fell behind**

```
Two languages fell behind. One action caught them up.

Every missing phrase is drafted by AI, the confirmation shows each language and its cost before anything runs, and the drafts wait for a person to review them.

Full video in the first comment.

#Localization #Translation #SaaS
```

Upload `videos/x/catching-up-a-language.mp4`.

First comment: `https://youtu.be/SHHt8ebaH-g`

## Week 4, Monday (launch + 21)

**Video: ‹DontTranslate› in Svelte: keep brand names verbatim**

```
Nobody wants their brand name translated.

‹DontTranslate› keeps it exactly as written, right where it stands, and the sentence around it still translates.

Full video in the first comment.

#Svelte #i18n #Branding
```

Upload `videos/x/svelte/donttranslate.mp4`.

First comment: `https://youtu.be/YPyWNGdaAHw`

## Week 4, Tuesday (launch + 22)

**Short: Add German to a live store, with no deploy**

```
Your live store, now in German.

Added in the project settings, priced exactly before it ran, drafted in seconds. No release, no deploy.

#Localization #Ecommerce #SaaS
```

Upload `videos/shared/social/add-german-1x1.mp4`.

First comment: `https://youtu.be/7dz7DjTAh2Y`

## Week 4, Wednesday (launch + 23)

**Video: Translating a whole content block as one**

```
A whole region of your app, translated as one block, one segment at a time.

AI drafts every segment together, a reviewer rewrites one in the formal register, and the sentence marked "don't translate" stays exactly as it was.

Full video in the first comment.

#Localization #Translation #SaaS
```

Upload `videos/x/translating-a-content-block.mp4`.

First comment: `https://youtu.be/YVYgEaPvcjg`

> On hold: Filmed against translation-manager MR !2; until it ships, the live app drops a segment edit and needs a reload to show the AI result. Post only once the video is public.

## Week 4, Thursday (launch + 24)

**Short: Two languages behind, caught up in one action**

```
French and Japanese fell behind. One action caught them up.

The drafts wait for review, so nothing reaches your users until a person has looked at it.

#Localization #Translation #SaaS
```

Upload `videos/shared/social/catch-up-1x1.mp4`.

First comment: `https://youtu.be/_3WJQCtVcdE`

## Week 4, Friday (launch + 25)

**Video: What is a content block? Translating a whole section in Svelte**

```
What is a content block?

A whole section registered as one unit, so it's translated with its context, and still made of phrases you can reuse anywhere else in the app.

Full video in the first comment.

#Svelte #i18n #WebDev
```

Upload `videos/x/svelte/content-blocks.mp4`.

First comment: `https://youtu.be/-ZMV0UyKRVk`

## Week 5, Monday (launch + 28)

**Video: AI Translator settings, every switch explained**

```
Every switch in the AI Translator, explained.

Including the one that spots a phrase that's already in Spanish and leaves it alone, so nobody pays to translate Spanish into Spanish.

You decide how much the model does: drafts on request, every new phrase automatically, or nothing until a person asks.

#AI #Localization #SaaS
```

Upload `videos/x/ai-translator-settings.mp4`.

First comment: `https://youtu.be/PnRoVVfYmKE`

## Week 5, Tuesday (launch + 29)

**Short: Translate a whole section with one tag**

```
Translate a whole section with one tag.

Bold and links land where they belong in each language, and the brand name stays put.

#i18n #Localization #WebDev
```

Upload `videos/svelte/social/content-blocks-1x1.mp4`.

First comment: `https://youtu.be/zw9iKNfjVng`

## Week 5, Wednesday (launch + 30)

**Video: Same word, two meanings: categories instead of i18n keys**

```
"Free" is a price. "Free" is also an empty evening.

In Spanish those are two different words: gratis and libre. Most i18n tools make a developer invent a key to tell them apart. Langsys files each under a category, and the translator sees which one they're translating.

Full video in the first comment.

#Localization #i18n #WebDev
```

Upload `videos/x/svelte/categories.mp4`.

First comment: `https://youtu.be/-P963Wj0dno`

## Week 5, Thursday (launch + 31)

**Short: Your brand name, never translated**

```
Bright Ledger, in Spanish: Libro Mayor Brillante.

That's what happens to a brand name nobody marked. A translator, human or AI, can't always tell a product name from a phrase.

With Langsys you mark it once, where it stands, and the sentence around it still translates.

#Branding #Localization #i18n
```

Upload `videos/svelte/social/brand-names-1x1.mp4`.

First comment: `https://youtu.be/dqxuUR7f7bs`

## Week 5, Friday (launch + 32)

**Video: API keys in production: activity, pausing and rotation**

```
What happens to an API key after it ships?

Its activity, a pause without deleting it, and a rotation that adds the new key before retiring the old one, so nothing in production goes dark.

Full video in the first comment.

#Security #DevOps #SaaS
```

Upload `videos/x/api-keys-in-production.mp4`.

First comment: `https://youtu.be/jZJRja7n_-c`

## Week 6, Monday (launch + 35)

**Video: Gender agreement without conditionals in your code (ICU select)**

```
¡Bienvenido, Diego! ¡Bienvenida, Laura!

Spanish agrees with the person. Most apps either branch on gender in the code or settle for one form for everyone.

Langsys builds the gender forms each language needs, so your code never branches.

#i18n #Localization #WebDev
```

Upload `videos/x/svelte/icu-gender.mp4`.

First comment: `https://youtu.be/AfpNQtvugks`

## Week 6, Tuesday (launch + 36)

**Short: Bienvenido or Bienvenida? One line of code**

```
Bienvenido or Bienvenida?

Diego, Laura, and someone with no gender on record, all greeted correctly from one line of code.

#i18n #Localization #WebDev
```

Upload `videos/svelte/social/icu-gender-1x1.mp4`.

First comment: `https://youtu.be/6bMkgdK1GpU`

## Week 6, Wednesday (launch + 37)

**Video: One organization, many projects**

```
Agencies: one organization, many projects.

Set the languages, AI settings and billing once. Override them only where a client's project needs its own, and fund every project from one shared balance.

Full video in the first comment.

#Agency #Localization #SaaS
```

Upload `videos/x/one-organization-many-projects.mp4`.

First comment: `https://youtu.be/y1kGQkoZ3_w`

## Week 6, Thursday (launch + 38)

**Short: One English word, two Spanish translations**

```
One English word. Two Spanish translations.

Gratis for the price. Libre for the evening.

The translator sees which one they're translating, and no developer invents a key to tell them apart.

#Localization #Translation #i18n
```

Upload `videos/svelte/social/two-meanings-1x1.mp4`.

First comment: `https://youtu.be/xEubzXvE5js`

## Week 6, Friday (launch + 39)

**Video: Translating placeholders, alt text and aria labels in Svelte**

```
A form with a translated label and an English placeholder is a half-translated form.

Placeholders, image descriptions and the labels a screen reader announces are translated in the same pass as the text around them. Accessibility shouldn't stop at English.

Full video in the first comment.

#Accessibility #i18n #WebDev
```

Upload `videos/x/svelte/attributes.mp4`.

First comment: `https://youtu.be/w9TNoFQ2fpM`

## Week 7, Monday (launch + 42)

**Video: Usage and credits: how a project gets funded**

```
How does a project get funded in Langsys?

Units pay for the API, credits pay for the AI model, and one transfer moves money to the project that needs it. Every machine translation is a line in the project's history, and a monthly limit means nothing runs away.

Full video in the first comment.

#SaaS #Localization #FinOps
```

Upload `videos/x/usage-and-credits.mp4`.

First comment: `https://youtu.be/TOqn3rfDyGQ`

## Week 7, Tuesday (launch + 43)

**Short: Placeholders and alt text translate too**

```
Placeholders and alt text translate too.

Even the words a screen reader announces. The attribute nobody remembered is the one that stays in English.

#Accessibility #i18n #Localization
```

Upload `videos/svelte/social/alt-text-1x1.mp4`.

First comment: `https://youtu.be/hsb-VE3Kc3E`

## Week 7, Wednesday (launch + 44)

**Video: Numbers and dates in every locale with Svelte i18n**

```
1,234.5 in the US. 1.234,5 in Germany. 12,34,567 in India.

Every number and date in each locale's own format, without a branch in your code, and an order number that stays exactly as written.

Full video in the first comment.

#i18n #Localization #WebDev
```

Upload `videos/x/svelte/formatting.mp4`.

First comment: `https://youtu.be/Bc2h2bxaB9M`

## Week 7, Thursday (launch + 45)

**Short: Every number and date in each locale's format**

```
Pass an order number as a number, and Germany sees 1.048.576.

Pass it as a string, and it stays 1048576.

Prices and dates take each locale's format. Identifiers stay exactly as written.

#i18n #Localization #WebDev
```

Upload `videos/svelte/social/local-formats-1x1.mp4`.

First comment: `https://youtu.be/_9CfOA8txIU`

## Week 7, Friday (launch + 46)

**Video: Plans and payments in Langsys**

```
Plans, billing cycles, saved cards and every invoice, in one place.

The boring part of Langsys, done properly: cards shared with an organization or a single project, saved billing addresses, and every invoice filterable by organization or project.

Full video in the first comment.

#SaaS #Billing #Localization
```

Upload `videos/x/plans-and-payments.mp4`.

First comment: `https://youtu.be/3Lnmfo0T71Q`

## Week 8, Monday (launch + 49)

**Video: Notifications: what Langsys tells you, and where**

```
New phrases to translate, invitations, project access: what Langsys tells you, and where.

In the app, by email, or both, with one project allowed its own rules when it needs them.

Full video in the first comment.

#Localization #Translation #SaaS
```

Upload `videos/x/notifications.mp4`.

First comment: `https://youtu.be/gpSYSKrmVp0`
