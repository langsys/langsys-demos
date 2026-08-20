# Build-along — Svelte (shooting script)

**Audience:** a developer evaluating Langsys. Not a tutorial — they are deciding
whether this is worth an afternoon, not learning to handle plural edge cases.

**Goals, in order:** credibility first, signup second. The signup is *earned* by
a limitation the viewer watches happen, not asked for out of nowhere.

**Format:** screen recording of a real editor and browser, with a real voice.
This is deliberately **not** the frame-addressed HTML pipeline the other cuts
use — `renderFrame(f)` is right for 70 seconds of explanation and unusable for
eight minutes of building. There is no beat table here: the voice leads and the
picture is cut to it, which is the opposite of `narrate.py`.

**Target length:** 7–8 minutes. Longer answers a question this audience has not
asked yet.

**Talking points, not a read.** The lines below are what to *land*, not words to
recite. Reading a script aloud is exactly the tone this video exists to avoid.

---

## Act 1 — credibility, zero friction (~0:00–4:00)

### 0:00 Cold open

Finished app already running in StackBlitz. Click through English, Español,
Français, Deutsch. **Three seconds of silence first** — let it land before
talking.

> That's a Svelte app translating itself. No keys file, no extraction step,
> nothing redeployed. Here's the whole integration.

Nothing is installed and nothing is signed up for at this point. Say so.

### 0:30 `src/langsys.js` — the entire integration

Open it. Forty-one lines, and most of them are comments and locale labels.

- `export const locale = writable('en-US')` — a plain Svelte store *is* the
  locale store. Nothing Langsys-specific about it.
- `LangsysApp.init({ projectid, key, UserLocaleStore: locale })` — that is the
  whole setup.

> Two things. A store you already know how to write, and one init call.

### 1:00 `App.svelte` — the call

> ```
> {$t('Hello, {name}!', 'Greetings', { name })}
> ```
> The English sentence is the lookup key **and** the default. There is no id to
> invent, so there is nothing to keep in step.

**Say the absence out loud** — it is the product:

> Notice what I haven't done. I haven't created a translations file. I haven't
> run an extraction step. That file does not exist in this project.

### 1:30 Build it from empty (~90s of screen time)

Speed-ramp every install. Never sit through a progress bar.

```
npm create vite@latest   → Svelte
npm install langsys-js-svelte
```

Write `langsys.js` live (store + init), wrap one heading in `$t()`, save.
Switch locale. It translates.

### 3:00 The plural

The catalog line already in the app:

```
{count, plural, one {# new message} other {# new messages}}
```

Change the count, then switch locale. Different languages apply their own rules.

> I wrote one English sentence. I did not write the Russian rules — nobody has
> those in their head.

### 3:30 Locale switch, one more time

> Nothing rebuilt. Nothing redeployed. It resolves at runtime.

---

## The pivot (~4:00–4:30) — the most important 30 seconds

Type a sentence that has **never existed**:

```
{$t('Your trial ends tomorrow', 'Billing')}
```

Switch to Español. **It stays in English.** Do not cut away from this.

> This key is read-only. It can fetch translations. It cannot register a phrase
> that doesn't exist yet — and this one was invented ten seconds ago.

That is the limitation, stated plainly, on camera. It is also the reason to
sign up, and the viewer just found it rather than being told it.

---

## Act 2 — the signup, now earned (~4:30–7:00)

### 4:30 Own project, write key

In the Manager: create a project, generate a **write** key.

**Keep the key off screen while pasting.** Use a throwaway project and rotate it
after recording. `svelte/.env.example` warns about this already — StackBlitz
forks are shareable, so this half is a local clone, not the sandbox. Say that on
camera; it costs five seconds and it is exactly the instinct this audience has.

```
cp .env.example .env      # own project id + WRITE key
```

### 5:00 The same sentence

Reload. Switch to Español. It comes back translated.

**Latency must be honest.** If it takes fifteen seconds, either sit through it
or say "that took about fifteen seconds" over the cut. A silent jump cut here is
precisely what a skeptical evaluator assumes is a cheat.

### 5:45 Show the Manager

The phrase is there — its category, its locales, the machine translation that
arrived on its own.

> I never wrote that sentence anywhere except my own code. It registered itself
> the first time the code ran, and it was translated before I switched tabs.

That is the thing the explainer only *claims*. Here it is happening.

### 6:30 The one caveat worth volunteering

> A write key belongs in development. Ship the read-only one — it's safe in a
> public browser bundle, which is why the StackBlitz demo can exist at all.

Volunteering the security boundary buys more trust than omitting it.

---

## Close (~7:00–7:30)

- The same integration in React, Vue, Angular, Laravel, Symfony, Rails, Django —
  one screen, no walkthrough.
- StackBlitz link on screen, held long enough to type.
- `langsys.com`

---

## Production notes

- **Mid-video CTA, around 2:00:** *"pause and open the StackBlitz — you'll be in
  the same app I'm in."* Almost no product can offer that; use it.
- **Cut ruthlessly.** `npm install`, dev-server boot, and page reloads are dead
  air. Speed-ramp or cut.
- **Do not re-explain the explainer.** Beats 5–7 of `explainer.mp4` already
  assert discovery, key permissions and machine translation on arrival. This
  video's job is to prove them. Same claims, different verb.
- **Where this lives:** the finished recording does not belong in git — several
  hundred MB of screen capture is neither a master nor cheap regenerable output.
  Host it, and keep this script in the repo as the source of record.
