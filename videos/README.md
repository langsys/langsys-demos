# Demo videos

Rendered walkthroughs of the Langsys SDKs. Each one opens with the Langsys
intro and is narrated end to end.

All are **1280×720, H.264 / yuv420p, 30 fps, AAC 48 kHz stereo**, with
`+faststart` set so they begin playing before the whole file has downloaded.
Each `.mp4` has a matching `-still.png` to use as its poster frame.

## Start here

| Video | Length | What it argues |
|---|---|---|
| `explainer.mp4` | 75.6s | What Langsys **is**. An SDK in your app and a hosted Translation Manager, how a phrase registers itself by running, where translations come from, and what you get. Start a cold viewer here. |
| `workflow.mp4` | 27.6s | The problem. Translation lives outside your codebase and round-trips through a pipeline; Langsys deletes the pipeline. Framework-agnostic — no SDK syntax on screen. |

`explainer` is the one to lead with. Every other cut assumes you already know
what Langsys is and shows what a single API does; this is the only one that
answers the question a first-time viewer actually has, including the part none
of the others cover — that a phrase registers itself the first time your code
runs it, gets machine translated on arrival, and is corrected in place by a
human without a deploy.

## Svelte

| Video | Length | Covers |
|---|---|---|
| `svelte/hero.mp4` | 16.6s | The short pitch — one call, locale switch, gender agreement, every locale |
| `svelte/key-files.mp4` | 25.6s | Why per-locale key files rot, and what replaces them |
| `svelte/t-string.mp4` | 42.6s | `t(phrase, category, params)` — opens on the keys-file problem, then the three arguments, ICU placeholders, plurals |
| `svelte/phrase-tag.mp4` | 20.6s | `<Phrase>` — a phrase in markup, and why its params are `%name%` |
| `svelte/translate-tag.mp4` | 19.6s | `<Translate>` — one tag registers a whole region as separate phrases |
| `svelte/donttranslate.mp4` | 20.6s | `<DontTranslate>` — brand names and identifiers held back verbatim |

Suggested order for a learning path: `explainer` → `workflow` → `key-files` →
`t-string` → `phrase-tag` → `translate-tag` → `donttranslate`. The first three
establish what Langsys is and why the old way hurts; the rest are API reference
and can be linked directly from a docs section.

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
