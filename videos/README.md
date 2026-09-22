# Demo videos

Rendered walkthroughs of the Langsys SDKs, plus silent square and vertical
re-cuts for social. The 16×9 cuts open with the Langsys intro and are narrated
end to end; the social cuts do neither — see [Social cuts](#social-cuts).

The 16×9 cuts are **1280×720, H.264 / yuv420p, 30 fps, AAC 48 kHz stereo**, with
`+faststart` set so they begin playing before the whole file has downloaded.
Each has a matching `-still.png` to use as its poster frame: frame 0 of the
master for the kit-based cuts, the title card for the app tutorials.

`thumbnails/<name>.png` is a **YouTube thumbnail** (1280×720) for every 16×9
cut: an eyebrow, a hook of at most seven words with the claim in teal, the
Langsys mark, and the cut's own poster frame inset on the right, so the
thumbnail and the first second of playback agree. They are rendered from
`assets/thumbnails/` in the `langsys-demo-videos` repo; change the copy there
and re-render rather than editing the PNGs.

Every 16×9 cut now opens with the intro sting, then a **2.0s title card** naming
what the cut covers, before its first beat. The lengths below include both.

## Start here

| Video | Length | What it argues |
|---|---|---|
| `explainer.mp4` | 77.4s | What **is** Langsys? An SDK in your app (eighteen of them, one per framework) and a hosted Translation Manager at app.langsys.dev, how a phrase registers itself by running, and where translations come from — including the part only Langsys can claim, told against a clock: a writer publishes a blog post at 09:00 with no build and no write key, the first reader gets English at 09:01, Langsys reads and translates the page at 09:02, and a reader in Madrid gets Spanish at 09:03. Start a cold viewer here. |

| `getting-started.mp4` | 253.1s | End to end in one take: create the project (organization, name and description, English as the source locale, Spanish, French and Japanese, auto-translate switched on), the app's own jump to the new project's API Keys page, a Read & Write key created and shown once, then the SDK: one install, one init, two env lines, the demo's `App.jsx` beside the running app with `t()`, the flat plural `t()`, `<Translate>`, `<Phrase>` and `<DontTranslate>` lit one at a time while the load registers the phrases, a cut back to the Translation Manager on the narrator's word, the phrases filed by category with the Spanish already in, the project dashboard at full coverage, and back in the app the locale pills switching to Spanish and French with no reload |
| `managing-translations.mp4` | 186.1s | The Manager on its own, for the person who owns the copy, with no code on screen: the Translations page and its to-do list, one machine draft opened, the cart line's `carrito` corrected to `cesta` (the word Spain uses) by deleting one word, Update Memory switched on, Save, the badge changing from the model's name to a person's, then the two phrases waiting in the queue: AI Translate drafts and saves the first and Auto-next carries the editor straight to the second, a look back at the first with the model's Spanish and badge, then the second typed and saved by hand, Never Translate explained, the React demo switched to Spanish with the correction live and nothing deployed, and Manage Access with a Translator invited to Spanish only |
| `translation-memory.mp4` | 167.4s | The sequel to `managing-translations`, and what its Update Memory switch bought: the Store's corrected cart line, then a second project, Selvara Outlet, made in the same wizard with Spanish as its only target and the cursor resting on the Locales tab's Use Translation Memory switch (on, inherited from the organization), a write key made off camera, the React demo loading against the new project, and the Manager showing the Outlet full before anyone has opened it: the cart line already reads `cesta` with Joe's badge, because memory carries who wrote a translation along with the words, the greeting is in with the model's badge from memory too, no model was called for the project at all, and the demo switches to Spanish with `cesta` live. Organization-wide, one entry per sentence per language |
| `usage-and-credits.mp4` | 142.0s | The two meters and how a project gets funded: Billing's overview with the account's own balance, the Subscription page with this month's API usage units against the plan's allowance, the Credits page at the account scope (prepaid and free credits, Add Credits named as the card path), a Transfer of $20 prepaid and $5 free to the Selvara Store done on camera and the account dropping by exactly that, the scope switched to the Store (balance up, usage summary, the transfer at the top of its transactions, one line per machine translation under it), and the project's Billing tab with the monthly credit limit and auto recharge. Page loads behind a dip, no app splash |
| `adding-a-language.mp4` | 109.2s | German added to a live project: the store's Deutsch pill that shows English because the project has no German, the "when a language is added" policy set to ask first, German picked under Locales, and on Save the dialog that prices the existing catalog exactly (29 words, $0.35) and asks; Translate, then the dashboard with German at 100%, the Manager's German draft with the model's badge, and the store switched to German with nothing built or deployed |
| `one-organization-many-projects.mp4` | 108.4s | The organization as the thing every project starts from: the switcher, the Organizations page, the organization's default Locales, AI Translator and Billing settings with Project Funding (whether projects may draw from its balance, and how much a month), a project whose Billing tab is customized switched back to inheriting through the app's confirmation, the projects list side by side, and the Credits page by scope with a project's draws from the organization. Re-shot 2026-09-09: the Credits page at the Store scope shows a real balance and the transfers that came in; page loads behind a dip, no app splash |
| `ai-translator-settings.mp4` | 144.2s | The AI Translator tab top to bottom, every switch explained and shown: Custom for this project switched off brings up the Clear Custom Settings dialog, cancelled; Use AI Translations shown in the Manager, where AI Translate on a phrase with no draft brings the model's draft on demand; auto-translate off and a phrase that arrives waits in the to-do list with no draft, on and the next phrase is drafted in seconds; auto-detect on and a phrase that arrives already in Spanish is held as never-translate by itself; the added-language policy pointed to its own video. Page loads behind a dip, no app splash |
| `connect-your-ai-assistant.mp4` | 106.8s | Langsys inside an AI assistant, over the hosted MCP server: the documented `claude mcp add` command with its real output, a question typed to the assistant, the browser opening on app.langsys.dev's Authorize Access screen (what the connection gets, that it is listed among your sessions and can be revoked there, that your password is never shared), Approve, then a real Claude Code answer made over the token that approval minted, listing the Store's four languages and how complete each is, the same numbers on the project dashboard, and the connection terminated from the account's Security tab, which retires the token. The answer card shows Claude's reply through its table; the rest is elided |
| `api-keys-in-production.mp4` | 89.7s | A key after it ships: the Store's API Keys page, the traffic key's Activity page with a real week of storefront reads (total API usage units and requests over a date range of up to 90 days), a description added to the key and the Active switch that pauses one without deleting it, then rotation on camera: a new Read Only key created with its secret shown once, and the old key deleted through the warning that access stops immediately. The charts under the totals are never on screen, because they do not render on the live app; both demo keys were revoked after the take |
| `catching-up-a-language.mp4` | 89.6s | The Manager's bulk actions for a language that fell behind: the Store's dashboard with French and Japanese each two phrases short, French picked in the Manager with its to-do list, the "..." menu with AI Translate Pending for this locale and the Clear Translations and Delete All Items actions pointed at but never pressed, AI Translate Pending run for French and a phrase opened with the model's draft, then the same action for the entire project, whose confirmation lists every target locale and warns that AI translation has a cost per word per locale, and the dashboard with every language complete |
| `plans-and-payments.mp4` | 86.1s | Billing as a tour of what is on file, with nothing submitted: the Subscription page with the organization's plan, billing cycle, this month's API usage units and billing address, the Change Plan dialog comparing Free Forever with Business and its billing cycle and card form, Payment Methods with sharing a card with an organization or project and the add-card dialog, Addresses, and Invoices with its scope and type filters. Every dialog is cancelled; the billing address on screen is the demo store's |
| `notifications.mp4` | 73.3s | Notifications from the user menu: the inbox with its unread and read filters, then the settings drawer with account defaults for new phrases, invitations and being added to a project or organization, each by in-app and email, email switched off for new phrases, a per-project override for the Store turned on with email back on for that project, and switched off again so the project follows the account defaults. The inbox is empty on camera; the account's settings were restored after the take |
| `translating-a-content-block.mp4` | 82.1s | A `<Translate>` region as one content block: the demo's two regions in code, then the Manager in Italian, a language added for the take with nothing translated, the Home block with the original beside the untranslated Italian and its two segments, the block's AI Translate filling both, and the Tour block whose `<DontTranslate>` sentence is struck through and stays in English while AI Translate fills in the Italian around it. Manual segment edits are not shown: the block editor's Save does not keep them on the live app. The editor also does not repaint the block after its AI Translate, so each result is shown after a reload behind a dip to black (the jump from English to Italian at ~0:42 is that reload, not an edit); once the editor repaints on its own, the dip goes and this take is worth re-shooting. Italian was removed after the take |
| `pluralization.mp4` | 73.6s | ICU plurals, from the beginning — why a sentence changes with its number at all, why the `if (count === 1)` that fixes it in English is English grammar in your code, and how writing the sentence **flat** gets you every branch in every language: translated flat first, then rebuilt in that locale's own categories (your English included). Framework-agnostic. |

`getting-started`, `managing-translations`, `translation-memory`, `usage-and-credits`, `adding-a-language`, `one-organization-many-projects`, `ai-translator-settings`, `connect-your-ai-assistant`, `api-keys-in-production`, `catching-up-a-language`, `plans-and-payments`, `notifications` and `translating-a-content-block` are tutorials, not synthetic cuts: each is one continuous recording
of the real app at app.langsys.dev and the React demo in this repo, driven by
a scripted browser, fronted with the same intro sting and a title card like
every other video, closed on the same outro card, and narrated by the same voice. Dead air is cut by rule at render time: a hold between two lines, or after the closing line, on picture that is not moving (cursor aside) is collapsed to under two seconds, so what remains of every pause is a page loading, text being typed, or a dialog opening. Filmed with throwaway keys that were revoked after the takes; the key on screen in `getting-started` is dead, and `managing-translations` and `translation-memory` never show one (the Outlet's write key was made through the API and revoked after the take). Its invite dialog is filled but Send is never pressed: the live API answered 404 on the invite endpoint at filming time. The key dialog shows the two access types the app offers today; `keys-and-environments.mp4` teaches a third, `ip_write`, which arrives with the write-key-gating release, and this take will need re-shooting then.

`explainer` is the one to lead with. Every other cut assumes you already know
what Langsys is and shows what a single API does; this is the only one that
answers the question a first-time viewer actually has, including the part none
of the others cover — that a phrase registers itself the first time your code
runs it, is machine-translated on arrival, and can be sharpened in place by a
translator without a deploy.

## Tutorial track

Ordered modules of the learning-center track. Watch them in this order; each one
assumes the previous. No SDK-specific syntax on screen.

| Video | Length | Covers |
|---|---|---|
| `tutorial/workflow.mp4` | 29.6s | The problem — translation round-trips through a pipeline, and Langsys deletes it |
| `tutorial/key-files.mp4` | 41.6s | Where a project starts, the key other i18n makes you invent, and what replaces it |
| `tutorial/locale-store.mp4` | 35.6s | The locale store — how the active locale is held and switched |
| `tutorial/keys-and-environments.mp4` | 90.4s | Keys from the ground up: why a key that can register can never ship, why read-only is a dead end, what `ip_write` is — one key whose answer depends on where you ask from — how you list the IP addresses your team browses from and what that buys, and which key goes where (write stays on machines you own, ip-write goes into any public bundle, read-only is for bundles that must never change anything). Then the 09:00 blog post: the two questions on startup, what leaves the browser (the address, never the text), Langsys visiting from an address the key trusts, the same SDK now write-enabled, and who else registers directly |
| `tutorial/adding-a-locale.mp4` | 29.6s | Reaching a new language is a project setting — new phrases translate on arrival, one run fills the rest |

## Svelte

| Video | Length | Covers |
|---|---|---|
| `svelte/hero.mp4` | 60.1s | The full walkthrough — what other i18n makes you keep in step, one call, a locale switch, why flat Spanish is wrong for half your users, and what ICU select does about it |
| `svelte/presenter.mp4` | 25.0s | **Proof of concept** — the hero's pitch delivered to camera in 25 seconds: a presenter in the left column, the code and the live app on the right, six lines (one import one call, the phrase is the key, the locale switch, *Bienvenido* for Diego, no branch written). The presenter is a stylised character animated from the narration, standing in for the recorded talent or licensed avatar the slot is built for; no intro sting |
| `svelte/t-string.mp4` | 69.3s | `t(phrase, category, params)` — opens on the keys-file problem, then the three arguments, ICU placeholders, plurals |
| `svelte/phrase-tag.mp4` | 66.3s | `<Phrase>` — a sentence with markup inside it, kept as one phrase, and why its params are `%name%` |
| `svelte/translate-tag.mp4` | 63.6s | `<Translate>` — one tag registers a whole region, and why a block beats a call per line |
| `svelte/donttranslate.mp4` | 33.6s | `<DontTranslate>` — brand names and identifiers held back verbatim, without hoisting them out of the sentence |
| `svelte/content-blocks.mp4` | 41.6s | What a content block *is* — one section registered as a unit, still made of individually reusable phrases |
| `svelte/categories.mp4` | 34.1s | Why i18n invented keys, and what replaces them — the same word, two meanings, and the pairs it splits into |
| `svelte/icu-gender.mp4` | 39.1s | Gender agreement — the conditional other i18n leaves in your component, and the branches Langsys generates instead |
| `svelte/attributes.mp4` | 66.8s | What an HTML attribute is, what a half-translated form looks like to the person hitting it, and how one `<Translate>` reaches placeholders, alt text and aria labels in the same pass |
| `svelte/formatting.mp4` | 46.4s | Numbers and dates per CLDR — the branch you write by hand, why grouping is a shape and not a separator, and why an order number must be passed as a string |

Suggested order: `explainer` first, then the tutorial track in the order above,
then the Svelte cuts as API reference — those can be linked directly from a docs
section rather than watched through.

## Social cuts

Square and vertical re-cuts of four Svelte demos, sized for feed and story
placements. **1080×1080 (`-1x1`) and 1080×1350 (`-4x5`), H.264 / yuv420p,
30 fps, `+faststart`** — the same encode as the 16×9 cuts apart from the frame
size.

Three things differ beyond the aspect ratio. They carry **no audio track** —
they are built to autoplay muted, and the caption on screen does the work the
voice-over does elsewhere. Each has a poster per ratio — `<demo>-4x5-still.png`
(1080×1350) and `<demo>-1x1-still.png` (1080×1080), frame 0 with the headline
caption on screen — for the `poster` attribute and as the thumbnail a platform
asks for at upload. And they skip the intro sting: each opens straight on its
first beat and closes on its own outro card.

| Video | Length | Covers |
|---|---|---|
| `svelte/social/phrase-{1x1,4x5}.mp4` | 12.0s | The phrase in your code *is* the key — no keys file, nothing to extract or keep in sync |
| `svelte/social/icu-gender-{1x1,4x5}.mp4` | 13.0s | *Bienvenido*, *Bienvenida*, and the neutral branch — generated by Langsys, not written by you |
| `svelte/social/content-blocks-{1x1,4x5}.mp4` | 14.0s | One tag over a whole region — every text run its own phrase, the brand name held back |
| `svelte/social/icu-plurals-{1x1,4x5}.mp4` | 14.0s | Russian's four plural forms off a single number, and English's two from the same line |

`icu-plurals` exists only as a social cut — there is no 16×9 version of it. The
framework-agnostic `pluralization.mp4` above covers the same ground at length.

## Where these come from

These are rendered output. The masters are single self-contained HTML files in
the **`langsys-demo-videos`** repo — open one and it plays, pass `?frame=N` and
it freezes on an exact frame, which is what makes frame-by-frame capture
reproducible. Fix copy there and re-render; do not edit the MP4s.

The API shown in each was checked against `svelte/src/App.svelte` in this repo
and the docs snippets, not written from memory — including the detail that
`t()` interpolates with `{name}` while `<Phrase>` uses `%name%`, because braces
are Svelte's own interpolation and would be consumed before Langsys saw them.

## Narration

The voice-over is generated speech — `en-US-AndrewMultilingualNeural` on
every narrated cut, the voice the explainer was cut with. A multilingual voice,
so the Spanish lines are pronounced correctly rather than read as English. Good enough for docs and the learning centre; anything
front-page or paid deserves a real read, and the scripts and per-beat timings
carry over directly.

The product name is said **"Lang-sis"**. The voice reads the written spelling
as "Lang-sees", and edge-tts takes no phonetic markup, so the scripts and
captions keep "Langsys" while the text handed to the voice says "Langsis", the
respelling the team picked by ear from six samples. The build refuses to
synthesize any line that would still give the voice the written name. For a
real read, brief the voice actor on the same pronunciation.

Each act is synthesized as **one continuous utterance** rather than line by
line, so intonation carries across it and the pauses are the voice's own.
Line-at-a-time synthesis gives every sentence a fresh start and a full
sentence-final fall, then dead air until the next beat — it sounds like someone
reading the captions aloud rather than explaining something.

The lines are still checked individually against the pictures they describe,
in both directions: one that overruns narrates the next scene, and one written
short pulls every line after it early onto the previous scene. The build reports
both and currently passes clean on all eight.
