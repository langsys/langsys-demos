# Demo videos

Rendered walkthroughs of the Langsys SDKs, plus silent square and vertical
re-cuts for social. The 16×9 cuts open with the Langsys intro and are narrated
end to end; the social cuts do neither — see [Social cuts](#social-cuts).

The 16×9 cuts are **1280×720, H.264 / yuv420p, 30 fps, AAC 48 kHz stereo**, with
`+faststart` set so they begin playing before the whole file has downloaded.
Each has a matching `-still.png` to use as its poster frame.

Every 16×9 cut now opens with the intro sting, then a **2.0s title card** naming
what the cut covers, before its first beat. The lengths below include both.

## Start here

| Video | Length | What it argues |
|---|---|---|
| `explainer.mp4` | 62.4s | What **is** Langsys? An SDK in your app and a hosted Translation Manager, how a phrase registers itself by running, and where translations come from. Start a cold viewer here. |

| `pluralization.mp4` | 73.6s | ICU plurals, from the beginning — why a sentence changes with its number at all, why the `if (count === 1)` that fixes it in English is English grammar in your code, and how writing the sentence **flat** gets you every branch in every language: translated flat first, then rebuilt in that locale's own categories (your English included). Framework-agnostic. |

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
| `tutorial/keys-and-environments.mp4` | 37.6s | Write keys in development, read-only keys in production |
| `tutorial/adding-a-locale.mp4` | 29.6s | Reaching a new language is a project setting — new phrases translate on arrival, one run fills the rest |

## Svelte

| Video | Length | Covers |
|---|---|---|
| `svelte/hero.mp4` | 60.1s | The full walkthrough — what other i18n makes you keep in step, one call, a locale switch, why flat Spanish is wrong for half your users, and what ICU select does about it |
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
voice-over does elsewhere. They have **no `-still.png`**, so set a `poster` only
if you generate one. And they skip the intro sting: each opens straight on its
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

The voice-over is generated speech — `en-US-EmmaMultilingualNeural` on the
feature cuts, `en-US-AndrewMultilingualNeural` on `explainer`. Both are
multilingual voices, so the Spanish lines are pronounced correctly rather than
read as English. Good enough for docs and the learning centre; anything
front-page or paid deserves a real read, and the scripts and per-beat timings
carry over directly.

Each act is synthesized as **one continuous utterance** rather than line by
line, so intonation carries across it and the pauses are the voice's own.
Line-at-a-time synthesis gives every sentence a fresh start and a full
sentence-final fall, then dead air until the next beat — it sounds like someone
reading the captions aloud rather than explaining something.

The lines are still checked individually against the pictures they describe,
in both directions: one that overruns narrates the next scene, and one written
short pulls every line after it early onto the previous scene. The build reports
both and currently passes clean on all eight.
