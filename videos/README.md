# Demo videos

Rendered walkthroughs of the Langsys SDKs. Each one opens with the Langsys
intro and is narrated end to end.

All are **1280×720, H.264 / yuv420p, 30 fps, AAC 48 kHz stereo**, with
`+faststart` set so they begin playing before the whole file has downloaded.
Each `.mp4` has a matching `-still.png` to use as its poster frame.

## Start here

| Video | Length | What it argues |
|---|---|---|
| `explainer.mp4` | 71.1s | What Langsys **is**. An SDK in your app and a hosted Translation Manager, how a phrase registers itself by running, where translations come from, and what you get. Start a cold viewer here. |

| `pluralization.mp4` | 20.6s | ICU plurals — one phrase carries the count, and Russian's four categories resolve from the same line. Framework-agnostic. |

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
| `tutorial/workflow.mp4` | 27.6s | The problem — translation round-trips through a pipeline, and Langsys deletes it |
| `tutorial/key-files.mp4` | 25.6s | Why per-locale key files rot, and what replaces them |
| `tutorial/locale-store.mp4` | 33.6s | The locale store — how the active locale is held and switched |
| `tutorial/keys-and-environments.mp4` | 35.6s | Write keys in development, read-only keys in production |
| `tutorial/adding-a-locale.mp4` | 27.6s | Reaching a new language is a project setting — new phrases translate on arrival, one run fills the rest |

## Svelte

| Video | Length | Covers |
|---|---|---|
| `svelte/hero.mp4` | 16.6s | The short pitch — one call, locale switch, gender agreement, every locale |
| `svelte/t-string.mp4` | 42.6s | `t(phrase, category, params)` — opens on the keys-file problem, then the three arguments, ICU placeholders, plurals |
| `svelte/phrase-tag.mp4` | 20.6s | `<Phrase>` — a phrase in markup, and why its params are `%name%` |
| `svelte/translate-tag.mp4` | 19.6s | `<Translate>` — one tag registers a whole region as separate phrases |
| `svelte/donttranslate.mp4` | 20.6s | `<DontTranslate>` — brand names and identifiers held back verbatim |
| `svelte/content-blocks.mp4` | 21.6s | `<Translate>` over a whole component — you never touch the markup inside |
| `svelte/categories.mp4` | 25.6s | Why i18n invented keys, and what replaces them — the same word, two meanings |
| `svelte/icu-gender.mp4` | 24.6s | Gender agreement — *Bienvenido* / *Bienvenida*, branches Langsys generates |

Suggested order: `explainer` first, then the tutorial track in the order above,
then the Svelte cuts as API reference — those can be linked directly from a docs
section rather than watched through.

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
