# X clips

Captioned 30 to 60 second clips of the long videos, one per X post (`x/posts.md`).

- Translation Manager clips: `videos/x/<name>.mp4`, cut by `clip.py`.
- Svelte clips: `videos/x/svelte/<name>.mp4`, trimmed after the intro sting. They need no captions because the video already has them.

## Re-cutting a Translation Manager clip

```
python transcribe.py                      # Whisper word timings -> <name>.json (skips existing)
python clip.py <name> --captions          # timed captions, to pick a window
python clip.py <name> <start> <end>       # render videos/x/<name>.mp4
```

The caption words come from `narrate_tour.py`'s SCRIPTS in langsys-demo-videos, so the spelling is exact. Whisper only supplies the timing. Requires `openai-whisper` and `imageio-ffmpeg`.

| Clip | Window (s) | Moment |
|---|---|---|
| managing-translations | 34.0–75.6 | AI draft, *carrito* changed to *cesta*, the badge changes to a person |
| translation-memory | 101.5–152.0 | new project already translated, Joe's badge carried over, no model called |
| adding-a-language | 47.8–96.8 | exact price, German drafted in seconds, nothing deployed |
| catching-up-a-language | 5.0–48.0 | two languages behind, one action, drafts waiting for review |
| translating-a-content-block | 36.2–94.2 | segments drafted together, one edited by hand, the Don't Translate sentence kept |
| ai-translator-settings | 64.2–123.0 | auto-translate off, then on, auto-detect catching a phrase that's already Spanish |
| api-keys-in-production | 46.6–100.4 | rotation: key types, ship IP write, copy the secret, delete the old key |
| one-organization-many-projects | 55.6–105.5 | override switched off, projects side by side, credits per scope |
| usage-and-credits | 43.0–94.0 | credits pay for the model, a transfer funds the Store |
| plans-and-payments | 16.6–73.6 | plans, billing cycle, saved cards, addresses, invoices |
| notifications | 22.1–68.8 | three kinds, app or email, one project's override |
