"""
Narrate the 9:16 YouTube Shorts cuts of the social demos.

The social cuts are silent because LinkedIn and X autoplay muted. Shorts play
with sound on, so the 9:16 cut of each social master carries the library's
narrator — the same voice and rate as every web cut — and no intro sting:
a Short has to open on its payoff, and three seconds of logo is where the
thumb leaves.

Same contract as narrate.py, whose helpers this reuses: one sentence per
line, each line placed on its own window, and the report's problem count has
to be zero. These masters cut every ~3s, so most windows hold about ten words;
write to that rather than stretching the master, because the 4:5 and 1:1 cuts
share its timing.

    python assets/capture.py svelte/social/phrase --ratio=9x16
    python assets/narration/narrate_shorts.py phrase

Output: <sdk>/social/<demo>/<demo>-9x16.mp4 (1080x1920, H.264 + AAC).
"""

import asyncio
import os
import sys
import wave

import numpy as np
from scipy import signal

from narrate import (BASE, FF, LEAD, REPO, SR, VO_GAIN, VOICE, clean, fades,
                     read_wav, run, synth_group)

# A notch quicker than the web cuts' +15%: Shorts are watched at feed pace,
# and these windows are about three seconds each.
RATE = "+20%"

# Spoken over the outro card. The short form is for the masters whose outro
# runs under two seconds.
CLOSE = "Try it free at langsys dot dev."
CLOSE_SHORT = "Langsys dot dev."

SHORTS = [
    dict(name="phrase", dir=r"svelte\social\phrase", secs=12,
         groups=[2, 2],
         starts=[0, 3.2, 6.6, 9.8],
         lines=[
             "With Langsys, your key is the English sentence.",
             "There's no keys file to extract or keep in sync.",
             "Switch locale, and the same line speaks Spanish.",
             CLOSE,
         ]),
    dict(name="icu-gender", dir=r"svelte\social\icu-gender", secs=13,
         groups=[2, 2, 1],
         starts=[0, 3.4, 6.6, 9.4, 11.4],
         lines=[
             "Spanish agrees with the user, so Diego gets Bienvenido.",
             "Laura gets Bienvenida, from the very same line of code.",
             "With no gender on record, you get the neutral form.",
             "And English needs no branch at all.",
             CLOSE_SHORT,
         ]),
    # The three counting beats are one sentence: at 2.4s each they would only
    # fit fragments, and the captions already name each form.
    dict(name="icu-plurals", dir=r"svelte\social\icu-plurals", secs=14,
         groups=[2, 1, 1],
         starts=[0, 3.0, 10.6, 12.6],
         lines=[
             "Russian has four plural forms, picked by the number.",
             "Three takes one form, five takes a different one, and twenty-one goes right back to the singular.",
             "English has two, from that one number.",
             CLOSE_SHORT,
         ]),
    dict(name="content-blocks", dir=r"svelte\social\content-blocks", secs=14,
         groups=[4, 1],
         starts=[0, 3.4, 6.8, 10.2, 12.4],
         lines=[
             "With Langsys, one tag wraps a whole region of your markup.",
             "Every run of text inside it becomes its own phrase.",
             "Switch the locale, and the bold and the links land where they belong.",
             "And your brand name never gets translated.",
             CLOSE_SHORT,
         ]),
    # The ten Shorts that fill the Tuesday/Thursday slots: one per long video,
    # every claim taken from that video's own script. Same beat grid in all
    # ten masters: three 3.2s beats, a 2.8s beat, then the outro.
    dict(name="published-at-nine", dir=r"shared\social\published-at-nine", secs=14,
         groups=[2, 2, 1],
         starts=[0, 3.2, 6.4, 9.6, 12.4],
         lines=[
             "Published at nine, and read in Spanish at three past.",
             "Nobody built it, deployed it, or ran it.",
             "Its first reader's app sends Langsys only the address.",
             "Langsys reads it, and Madrid gets Spanish.",
             CLOSE_SHORT,
         ]),
    dict(name="ask-your-assistant", dir=r"shared\social\ask-your-assistant", secs=14,
         groups=[2, 2, 1],
         starts=[0, 3.2, 6.4, 9.6, 12.4],
         lines=[
             "Ask your AI assistant how your translations are doing.",
             "It reads the same numbers as your dashboard.",
             "Then ask it to translate what's missing, and it does.",
             "One approval, and never your password.",
             CLOSE_SHORT,
         ]),
    dict(name="memory", dir=r"shared\social\memory", secs=14,
         groups=[2, 2, 1],
         starts=[0, 3.2, 6.4, 9.6, 12.4],
         lines=[
             "A brand-new project, and it's already in Spanish.",
             "In another project, someone changed carrito to cesta.",
             "The new one already says cesta, and credits Joe.",
             "And no model was ever called.",
             CLOSE_SHORT,
         ]),
    dict(name="add-german", dir=r"shared\social\add-german", secs=14,
         groups=[2, 2, 1],
         starts=[0, 3.2, 6.4, 9.6, 12.4],
         lines=[
             "Your live store, now in German, with no deploy.",
             "You add German in settings, not in your code.",
             "Langsys quotes the exact price before it spends anything.",
             "Drafted in seconds, and German just works.",
             CLOSE_SHORT,
         ]),
    dict(name="catch-up", dir=r"shared\social\catch-up", secs=14,
         groups=[2, 2, 1],
         starts=[0, 3.2, 6.4, 9.6, 12.4],
         lines=[
             "Two languages fell behind, and one action caught them up.",
             "French and Japanese were each missing two phrases.",
             "AI Translate Pending drafts them in seconds.",
             "And the drafts wait for a review.",
             CLOSE_SHORT,
         ]),
    dict(name="brand-names", dir=r"svelte\social\brand-names", secs=14,
         groups=[2, 2, 1],
         starts=[0, 3.2, 6.4, 9.6, 12.4],
         lines=[
             "Your brand name, untouched in every language.",
             "Other i18n translates it, and renames your brand.",
             "Now with Langsys, you mark the name right where it stands.",
             "And the sentence around it still translates.",
             CLOSE_SHORT,
         ]),
    dict(name="two-meanings", dir=r"svelte\social\two-meanings", secs=14,
         groups=[2, 2, 1],
         starts=[0, 3.2, 6.4, 9.6, 12.4],
         lines=[
             "One English word, and two different Spanish translations.",
             "Other i18n invents a key just to tell them apart.",
             "Now with Langsys, a category tells them apart.",
             "Gratis is a price, libre a free evening.",
             CLOSE_SHORT,
         ]),
    dict(name="bold-moves", dir=r"svelte\social\bold-moves", secs=14,
         groups=[2, 2, 1],
         starts=[0, 3.2, 6.4, 9.6, 12.4],
         lines=[
             "In Spanish, your bold moves to where Spanish puts it.",
             "Other i18n cuts it into three keys.",
             "Now with Langsys, one tag wraps it, markup and all.",
             "One sentence, and the bold comes back.",
             CLOSE_SHORT,
         ]),
    dict(name="local-formats", dir=r"svelte\social\local-formats", secs=14,
         groups=[2, 2, 1],
         starts=[0, 3.2, 6.4, 9.6, 12.4],
         lines=[
             "Every number and date, in each locale's own format.",
             "Hindi doesn't even group its digits in threes.",
             "You pass the number itself, and the date as a date.",
             "An order number goes in as a string.",
             CLOSE_SHORT,
         ]),
    dict(name="alt-text", dir=r"svelte\social\alt-text", secs=14,
         groups=[2, 2, 1],
         starts=[0, 3.2, 6.4, 9.6, 12.4],
         lines=[
             "Placeholders and image descriptions translate too.",
             "Other i18n needs a call per attribute.",
             "Now with Langsys, one tag covers the whole region.",
             "Even what a screen reader announces.",
             CLOSE_SHORT,
         ]),
]


async def build(short):
    name, secs, starts, lines = short["name"], short["secs"], short["starts"], short["lines"]
    N = int(SR * secs)
    assert len(starts) == len(lines), f"{name}: {len(starts)} starts but {len(lines)} lines"

    body = os.path.join(BASE, f"body-{name}-9x16.mp4")
    if not os.path.exists(body):
        print(f"\n=== {name}  SKIPPED — no {body}")
        return 0

    vo_dir = os.path.join(BASE, f"vo-{name}-9x16")
    os.makedirs(vo_dir, exist_ok=True)
    print(f"\n=== {name}  ({secs:.1f}s, {VOICE})")

    # `groups` as in narrate.py: each run of lines is one utterance, anchored
    # on its first line's window. Absent, the whole Short is one breath.
    sizes = short.get("groups") or [len(lines)]
    assert sum(sizes) == len(lines), f"{name}: groups sum to {sum(sizes)}, not {len(lines)}"

    vo = np.zeros(N)
    problems = 0
    first = 0
    for g, size in enumerate(sizes):
        members = list(range(first, first + size))
        first += size

        mp3, wav = os.path.join(vo_dir, f"g{g}.mp3"), os.path.join(vo_dir, f"g{g}.wav")
        bounds = await synth_group([lines[i] for i in members], VOICE, mp3, RATE)
        run([FF, "-y", "-i", mp3, "-ar", str(SR), "-ac", "1", wav])
        x, sr0 = read_wav(wav)
        if x.ndim > 1:
            x = x.mean(axis=1)
        if sr0 != SR:
            x = signal.resample_poly(x, SR, sr0)
        x = fades(clean(x))

        head = bounds[0][0]
        t0 = starts[members[0]] + LEAD
        a = int((t0 - head) * SR)
        src = x[max(0, -a):]
        a = max(a, 0)
        b = min(a + len(src), N)
        vo[a:b] += src[:b - a] * VO_GAIN

        for k, i in enumerate(members):
            s = t0 + (bounds[k][0] - head)
            e = s + bounds[k][1]
            win0 = starts[i]
            win1 = starts[i + 1] if i + 1 < len(starts) else secs
            fill = bounds[k][1] / (win1 - win0) * 100
            early = s < win0 - 0.45
            late = s > win1 - 0.05
            # The last line has no next picture to spill into, only the end.
            over = e > win1 + (0.35 if i + 1 < len(starts) else 0.0)
            if early or late or over:
                problems += 1
            flag = ('STARTS EARLY by %.2fs' % (win0 - s) if early
                    else 'STARTS LATE' if late
                    else 'OVERRUNS by %.2fs' % (e - win1) if over else 'ok')
            print(f"   {i+1:2}  {s:6.2f} -> {e:6.2f}   beat {win0:6.2f}-{win1:6.2f}"
                  f"   fill {fill:3.0f}%   {flag}")

    out = np.stack([vo, vo], axis=1)
    tail = int(0.08 * SR)
    out[-tail:] *= np.linspace(1, 0, tail)[:, None]
    peak = np.max(np.abs(out))
    if peak > 0:
        out *= 10 ** (-1.5 / 20) / peak

    bed = os.path.join(BASE, f"bed-{name}-9x16.wav")
    with wave.open(bed, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())

    final = os.path.join(REPO, short["dir"], f"{name}-9x16.mp4")
    run([FF, "-y", "-i", body, "-i", bed,
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2",
         "-shortest", "-movflags", "+faststart", final])
    print(f"   -> {short['dir']}\\{name}-9x16.mp4   ({problems} problem{'' if problems == 1 else 's'})")
    return problems


async def main():
    only = sys.argv[1:]
    bad = 0
    for short in SHORTS:
        if only and short["name"] not in only:
            continue
        bad += await build(short)
    print(f"\n=== finished. {bad} line(s) off their window.")


if __name__ == "__main__":
    asyncio.run(main())
