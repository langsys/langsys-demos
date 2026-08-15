# Demo videos

Rendered walkthroughs of the Langsys SDKs. Each one opens with the Langsys
intro and is narrated end to end.

All are **1280×720, H.264 / yuv420p, 30 fps, AAC 48 kHz stereo**, with
`+faststart` set so they begin playing before the whole file has downloaded.
Each `.mp4` has a matching `-still.png` to use as its poster frame.

## Start here

| Video | Length | What it argues |
|---|---|---|
| `workflow.mp4` | 27.6s | The problem. Translation lives outside your codebase and round-trips through a pipeline; Langsys deletes the pipeline. Framework-agnostic — no SDK syntax on screen. |

## Svelte

| Video | Length | Covers |
|---|---|---|
| `svelte/hero.mp4` | 16.6s | The short pitch — one call, locale switch, gender agreement, every locale |
| `svelte/key-files.mp4` | 25.6s | Why per-locale key files rot, and what replaces them |
| `svelte/t-string.mp4` | 21.6s | `t(phrase, category, params)` — the inline call, ICU placeholders, plurals |
| `svelte/phrase-tag.mp4` | 20.6s | `<Phrase>` — a phrase in markup, and why its params are `%name%` |
| `svelte/translate-tag.mp4` | 19.6s | `<Translate>` — one tag registers a whole region as separate phrases |
| `svelte/donttranslate.mp4` | 20.6s | `<DontTranslate>` — brand names and identifiers held back verbatim |

Suggested order for a learning path: `workflow` → `key-files` → `t-string` →
`phrase-tag` → `translate-tag` → `donttranslate`. The first two establish the
problem; the rest are API reference and can be linked directly from a docs
section.

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

The voice-over is generated speech (Microsoft `en-US-EmmaMultilingualNeural`), a
multilingual voice so the Spanish lines are pronounced correctly rather than
read as English. It is good enough for docs and the learning centre. Anything
front-page or paid deserves a real read — the scripts and the per-beat timings
carry over directly.

Every line is placed on its demo's own scene boundary, offset by the intro
length. A line that runs past the scene it describes is narrating the wrong
picture, so the build checks each one against its window and fails loudly.
