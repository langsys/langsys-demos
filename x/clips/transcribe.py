import json, os, subprocess, sys
import numpy as np
import whisper
FF = os.path.expandvars(r"%USERPROFILE%/AppData/Roaming/Python/Python311/site-packages/imageio_ffmpeg/binaries/ffmpeg-win64-v4.2.2.exe")

def audio(path):
    raw = subprocess.run([FF, "-nostdin", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).flatten().astype(np.float32) / 32768.0

V = r"C:\laragon\www\langsys-demos\videos"
OUT = os.path.dirname(os.path.abspath(__file__))
NAMES = ["managing-translations", "translation-memory", "adding-a-language", "catching-up-a-language",
         "translating-a-content-block", "ai-translator-settings", "api-keys-in-production",
         "one-organization-many-projects", "usage-and-credits", "plans-and-payments", "notifications"]
model = whisper.load_model("small.en")
for name in NAMES:
    dest = os.path.join(OUT, f"{name}.json")
    if os.path.exists(dest):
        continue
    result = model.transcribe(audio(os.path.join(V, f"{name}.mp4")), word_timestamps=True, language="en",
                              initial_prompt="Langsys, Translation Manager, AI Translate, Translation Memory.")
    segs = [{"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip(),
             "words": [{"w": w["word"], "s": round(w["start"], 2), "e": round(w["end"], 2)} for w in s["words"]]}
            for s in result["segments"]]
    json.dump(segs, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(name, len(segs), "segments", flush=True)
