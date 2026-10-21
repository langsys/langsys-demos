"""Cut a captioned X clip from a Translation Manager video.

    python clip.py <video> <start> <end>       render videos/x/<video>.mp4
    python clip.py <video> --captions          print the timed captions, to pick a window

Caption words come from narrate_tour.py's SCRIPTS (exact spelling); their
timing comes from the Whisper transcript in this folder.
"""

import difflib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = r"C:\laragon\www\langsys-demos\videos"
TOUR = r"C:\laragon\www\langsys-demo-videos\assets\tour"
FONTS = r"C:\laragon\www\langsys-demo-videos\assets\logo\fonts"
FF = os.path.expandvars(r"%USERPROFILE%/AppData/Roaming/Python/Python311/site-packages/imageio_ffmpeg/binaries/ffmpeg-win64-v4.2.2.exe")

SCRIPT_KEYS = {
    "managing-translations": "tour-manager",
    "translation-memory": "tour-memory",
    "adding-a-language": "tour-addlang",
    "catching-up-a-language": "tour-catchup",
    "translating-a-content-block": "tour-blocks",
    "ai-translator-settings": "tour-ai",
    "api-keys-in-production": "tour-keys",
    "one-organization-many-projects": "tour-org",
    "usage-and-credits": "tour-credits",
    "plans-and-payments": "tour-plans",
    "notifications": "tour-notifications",
}

MAX_CHARS = 44
FADE = 0.3


def _script_lines(name):
    source = open(os.path.join(TOUR, "narrate_tour.py"), encoding="utf-8").read()
    start = source.index("SCRIPTS = {")
    end = source.index("\n}\n", start) + 3
    namespace = {}
    exec(source[start:end], namespace)
    lines = [text for group in namespace["SCRIPTS"][SCRIPT_KEYS[name]] for _, text in group]
    return [re.sub(r"\[\[es:([^\]]+)\]\]", r"\1", line) for line in lines]


def _norm(word):
    return re.sub(r"[^a-z0-9]", "", word.lower())


def _timed_words(name):
    heard = [word for segment in json.load(open(os.path.join(HERE, f"{name}.json"), encoding="utf-8"))
             for word in segment["words"]]
    written = []
    for index, line in enumerate(_script_lines(name)):
        for word in line.split():
            written.append({"w": word, "line": index})
    matcher = difflib.SequenceMatcher(a=[_norm(w["w"]) for w in written], b=[_norm(h["w"]) for h in heard],
                                      autojunk=False)
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            written[block.a + offset]["s"] = heard[block.b + offset]["s"]
            written[block.a + offset]["e"] = heard[block.b + offset]["e"]
    _interpolate(written)
    return written


def _interpolate(words):
    known = [i for i, w in enumerate(words) if "s" in w]
    for i, word in enumerate(words):
        if "s" in word:
            continue
        before = max((k for k in known if k < i), default=None)
        after = min((k for k in known if k > i), default=None)
        if before is None:
            word["s"] = word["e"] = words[after]["s"]
        elif after is None:
            word["s"] = word["e"] = words[before]["e"]
        else:
            span = (words[after]["s"] - words[before]["e"]) / (after - before)
            word["s"] = words[before]["e"] + span * (i - before - 1)
            word["e"] = word["s"] + span


def _split_line(words):
    """Balanced chunks of at most MAX_CHARS, breaking after punctuation when
    one is close to the even split, so no chunk is a lone trailing word."""
    text_length = len(" ".join(w["w"] for w in words))
    pieces = -(-text_length // MAX_CHARS)
    if pieces <= 1:
        return [words]
    target = text_length / pieces
    chunks, current = [], []
    for index, word in enumerate(words):
        current.append(word)
        length = len(" ".join(w["w"] for w in current))
        remaining = words[index + 1:]
        if not remaining:
            continue
        next_length = len(" ".join(w["w"] for w in current + [remaining[0]]))
        tail_length = len(" ".join(w["w"] for w in remaining))
        if next_length > MAX_CHARS:
            chunks.append(current)
            current = []
            continue
        if tail_length < 14 and length + 1 + tail_length <= MAX_CHARS + 6:
            continue
        clause_ahead = len(remaining[0]["w"]) <= 8 and remaining[0]["w"][-1] in ",.;:?!"
        at_punctuation = (word["w"][-1] in ",.;:?!" and length >= target * 0.6 and tail_length >= 14
                          and not clause_ahead)
        if at_punctuation or (length >= target and tail_length >= 14):
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks


def _captions(name):
    lines = {}
    for word in _timed_words(name):
        lines.setdefault(word["line"], []).append(word)
    chunks = [chunk for index in sorted(lines) for chunk in _split_line(lines[index])]
    return [{"s": c[0]["s"], "e": c[-1]["e"], "text": " ".join(w["w"] for w in c)} for c in chunks]


def _ass_time(seconds):
    seconds = max(seconds, 0)
    return f"{int(seconds // 3600)}:{int(seconds % 3600 // 60):02d}:{seconds % 60:05.2f}"


def _write_ass(captions, start, end, path):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Inter SemiBold,34,&H00FFFFFF,&H00FFFFFF,&H40140D0B,&H40140D0B,0,0,0,0,100,100,0,0,3,12,0,2,80,80,44,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    shown = [c for c in captions if c["e"] > start and c["s"] < end]
    for index, caption in enumerate(shown):
        following = shown[index + 1]["s"] if index + 1 < len(shown) else end
        caption_end = min(max(caption["e"] + 0.4, caption["s"] + 1.0), following, end)
        events.append(f"Dialogue: 0,{_ass_time(caption['s'] - start)},{_ass_time(caption_end - start)},Caption,,0,0,0,,{caption['text']}")
    open(path, "w", encoding="utf-8").write(header + "\n".join(events) + "\n")


def render(name, start, end):
    ass = os.path.join(HERE, f"{name}.ass")
    _write_ass(_captions(name), start, end, ass)
    length = end - start
    os.makedirs(os.path.join(VIDEOS, "x"), exist_ok=True)
    dest = os.path.join(VIDEOS, "x", f"{name}.mp4")
    escaped = ass.replace("\\", "/").replace(":", "\\:")
    fonts = FONTS.replace("\\", "/").replace(":", "\\:")
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{start}", "-i", os.path.join(VIDEOS, f"{name}.mp4"), "-t", f"{length}",
                    "-vf", f"subtitles='{escaped}':fontsdir='{fonts}',fade=t=in:d={FADE},fade=t=out:st={length - FADE}:d={FADE}",
                    "-af", f"afade=t=in:d={FADE},afade=t=out:st={length - FADE}:d={FADE}",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", dest], check=True)
    print(f"{name}: {start:.2f}-{end:.2f} ({length:.1f}s) -> {dest}")


if __name__ == "__main__":
    name = sys.argv[1]
    if sys.argv[2] == "--captions":
        for caption in _captions(name):
            print(f"{caption['s']:7.2f} {caption['e']:7.2f}  {caption['text']}")
    else:
        render(name, float(sys.argv[2]), float(sys.argv[3]))
