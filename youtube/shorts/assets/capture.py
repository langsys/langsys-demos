"""
Capture a demo's frames and encode the silent body.

This is step 2 and 3 of the README's render recipe, which were previously done
by hand. The explainer alone is 288 screenshots; doing that manually is why the
`social/` captions never got a second pass and why `pluralization` stopped at
59 of 68 frames. Anything that has to happen 100+ times per demo belongs here.

    python assets/capture.py locale-store
    python assets/capture.py                 # every demo with a master

Output goes to BASE\\body-<name>.mp4, which is exactly where narrate.py expects
to find it, so the full pipeline is:

    python assets/capture.py <name> && python assets/narration/narrate.py <name>

Frame counts are read out of the master itself (`fps:` and `seconds:` in the
LangsysWebDemo config), not passed in — the HTML is the master, so a demo whose
length changes must not also need this script edited. The masters that predate
the kit declare the same two names as uppercase consts, so the match is
case-insensitive.

Chrome's `--headless=new` hangs on this workload; the headless shell exits
cleanly per screenshot, so that is what this drives. The screenshot is of the
whole viewport rather than the #stage element, which is why the window size has
to match the stage exactly — a mismatch silently letterboxes every frame.
"""

import functools
import http.server
import os
import re
import shutil
import subprocess
import sys
import threading

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARRATE = os.path.join(REPO, "assets", "narration", "narrate.py")


def _scratch_dir():
    """Take BASE from narrate.py, which owns it.

    These two scripts hand off through BASE\\body-<name>.mp4, so a second copy
    of that path here is a silent-failure waiting to happen: narrate.py skips a
    demo whose body it cannot find and leaves the previous mp4 in place, which
    looks exactly like a successful no-op run (its own comment says so).

    Read rather than import — importing narrate.py pulls in edge_tts, numpy
    and scipy, none of which a capture needs.
    """
    src = open(NARRATE, encoding="utf-8").read()
    m = re.search(r'^BASE\s*=\s*r"([^"]+)"', src, re.M)
    if not m:
        raise SystemExit(f"could not read BASE from {NARRATE}")
    return m.group(1)

FF = os.path.expandvars(
    r"%USERPROFILE%\AppData\Roaming\Python\Python311\site-packages"
    r"\imageio_ffmpeg\binaries\ffmpeg-win64-v4.2.2.exe")

SHELL = os.path.expandvars(
    r"%LOCALAPPDATA%\ms-playwright\chromium_headless_shell-1208"
    r"\chrome-headless-shell-win64\chrome-headless-shell.exe")

PORT = 4455
# The `web/` capture stage. `social/` masters declare their own; pass --size.
SIZE = (1280, 720)


def serve():
    """Serve the repo root for the life of the process.

    Kit-based masters pull ../../../assets/web-kit.css, so file:// URLs render
    unstyled — and an unstyled capture fails silently rather than erroring,
    which is the expensive way to discover this.
    """
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory=REPO)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    httpd.log_message = lambda *a: None
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def find_master(name):
    """<sdk>/<placement>/<name>/<name>.html — the layout the README fixes.

    A bare name may match in more than one placement: `icu-gender` and
    `content-blocks` each exist as both a social and a web cut, and the two are
    different masters of different lengths, not crops of each other. Returning
    the first hit silently captured the 13s social master for a 21s web cut, so
    an ambiguous name is now an error and the caller passes the qualified path:

        python assets/capture.py svelte/web/icu-gender
    """
    if "/" in name or os.sep in name:
        rel = name.replace(os.sep, "/")
        leaf = rel.rsplit("/", 1)[-1]
        cand = os.path.join(REPO, *rel.split("/"), leaf + ".html")
        return (cand, rel) if os.path.exists(cand) else (None, None)

    hits = []
    for sdk in sorted(os.listdir(REPO)):
        sdk_dir = os.path.join(REPO, sdk)
        if not os.path.isdir(sdk_dir) or sdk.startswith(('.', 'frames', 'assets')):
            continue
        for placement in sorted(os.listdir(sdk_dir)):
            cand = os.path.join(sdk_dir, placement, name, name + ".html")
            if os.path.exists(cand):
                hits.append((cand, f"{sdk}/{placement}/{name}"))

    if len(hits) > 1:
        opts = [h[1] for h in hits]
        raise SystemExit(
            "'" + name + "' is ambiguous - it exists in "
            + str(len(hits)) + " placements:" + '\n  ' + '\n  '.join(opts)
            + '\n' + "Pass the qualified path instead, e.g. "
            + "python assets/capture.py " + opts[0])
    return hits[0] if hits else (None, None)


def frame_count(path):
    """Read fps and seconds out of the master. Returns (fps, seconds, total)."""
    src = open(path, encoding="utf-8").read()
    # Case-insensitive: kit demos declare `fps: 4`, the older self-contained
    # masters declare `const FPS = 4`. Same two names, different case.
    fps = re.search(r"\bfps\s*[:=]\s*([0-9.]+)", src, re.I)
    secs = re.search(r"\bseconds\s*[:=]\s*([0-9.]+)", src, re.I)
    if not fps or not secs:
        raise SystemExit(
            f"{path}: could not find `fps` and `seconds`. Both are declared "
            f"near the top of every master's script block - if this one names "
            f"them differently, rename rather than special-casing here.")
    fps, secs = float(fps.group(1)), float(secs.group(1))
    return fps, secs, int(round(fps * secs))


def capture(name, size=SIZE, tag="", query="", dest=None):
    master, rel = find_master(name)
    if not master:
        raise SystemExit(f"no master found for {name!r} "
                         f"(expected <sdk>/<placement>/{name}/{name}.html)")

    # `name` may be qualified (svelte/web/icu-gender) to disambiguate a demo
    # that exists in two placements. Everything downstream — the frames dir, the
    # url, the body handed to narrate.py — is keyed on the demo's own name, so
    # take the leaf. Leaving the slash in produced `frames-svelte/web/...`.
    name = rel.rsplit("/", 1)[-1]

    fps, secs, total = frame_count(master)
    frames = os.path.join(REPO, "frames-" + name + (("-" + tag) if tag else ""))
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames)

    url = f"http://127.0.0.1:{PORT}/{rel}/{name}.html"
    print(f"\n=== {name}  {fps:g} fps x {secs:g}s = {total} frames  ({size[0]}x{size[1]})")
    print(f"    {url}")

    for f in range(total):
        out = os.path.join(frames, f"{f:03d}.png")
        r = subprocess.run([
            SHELL, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--virtual-time-budget=1200",
            f"--window-size={size[0]},{size[1]}",
            f"--screenshot={out}", f"{url}?frame={f}{query}",
        ], capture_output=True)

        if not os.path.exists(out):
            raise SystemExit(
                f"\nframe {f} produced no file - capture aborted.\n"
                f"{r.stderr.decode('utf-8', 'replace')[-800:]}")

        if f % 20 == 0 or f == total - 1:
            print(f"    {f + 1}/{total}", flush=True)

    # A frame that renders unstyled still writes a valid PNG, so size is the
    # only cheap signal that the stylesheet resolved. A styled 1280x720 stage
    # lands far above this; an unstyled one is a mostly-white page.
    #
    # Median, not min. A master that fades in or out through black ends up with
    # a handful of near-solid frames that compress to a few KB, which is not a
    # stylesheet failure — and a check that fires on every render of such a cut
    # is a check nobody reads. An unstyled render is unstyled on every frame,
    # so the median catches it just as well.
    sizes = sorted(os.path.getsize(os.path.join(frames, p))
                   for p in os.listdir(frames))
    median = sizes[len(sizes) // 2]
    if median < 12_000:
        print(f"    ! median frame is {median} bytes - check the stylesheet "
              f"resolved before trusting this render")

    if dest:
        # Social cuts are silent and never fronted with the intro, so the
        # encode is the finished file and goes straight to the demo folder.
        body = dest
    else:
        base = _scratch_dir()
        os.makedirs(base, exist_ok=True)
        body = os.path.join(base, f"body-{name}" + (f"-{tag}" if tag else "") + ".mp4")
    subprocess.run([
        FF, "-y", "-framerate", str(fps),
        "-i", os.path.join(frames, "%03d.png"),
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart", body,
    ], capture_output=True, check=True)

    print(f"    -> {body}  ({os.path.getsize(body) // 1024}K)")
    return body


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    size = SIZE
    # --lang=es renders a master's language variant (`?lang=es`, see the
    # explainer) into frames-<name>-es and body-<name>-es.mp4, which is the
    # body narrate.py reads for its <name>-es entry.
    lang = ""
    # --ratio=9x16 renders just one of a social demo's cuts. Without it every
    # ratio is rendered, which rewrites the committed 4x5 / 1x1 files too.
    ratios = None
    for a in sys.argv[1:]:
        if a.startswith("--lang="):
            lang = a.split("=", 1)[1]
        if a.startswith("--ratio="):
            ratios = a.split("=", 1)[1].split(",")
        if a.startswith("--size="):
            w, h = a.split("=", 1)[1].split("x")
            size = (int(w), int(h))

    if not os.path.exists(SHELL):
        raise SystemExit(f"no headless shell at {SHELL}")
    if not os.path.exists(FF):
        raise SystemExit(f"no ffmpeg at {FF}")

    serve()
    for name in args:
        # A social demo is two cuts at two viewports, written as finished
        # -4x5 / -1x1 files rather than a body for narrate.py. Without this
        # they sit outside the automation, which is exactly how the langsys.dev
        # sweep re-rendered every web cut and silently left the social ones on
        # a four-month-old render showing the old domain.
        master, rel = find_master(name)
        if master and "/social/" in ("/" + (rel or "") + "/"):
            leaf = rel.rsplit("/", 1)[-1]
            folder = os.path.dirname(master)
            for tag, w, h, q in (("4x5", 1080, 1350, ""),
                                 ("1x1", 1080, 1080, "&ratio=1x1"),
                                 ("9x16", 1080, 1920, "&ratio=9x16")):
                if ratios and tag not in ratios:
                    continue
                # The Shorts cut is narrated, so it is a body for
                # narrate_shorts.py, not a finished file.
                dest = None if tag == "9x16" else os.path.join(folder, f"{leaf}-{tag}.mp4")
                capture(name, (w, h), tag=tag, query=q, dest=dest)
            continue

        capture(name, size, tag=lang, query=f"&lang={lang}" if lang else "")


if __name__ == "__main__":
    main()
