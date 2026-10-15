# YouTube channel assets

Branding for the official Langsys YouTube channel, [youtube.com/@Langsys](https://www.youtube.com/@Langsys). The videos themselves live in [`../videos`](../videos), with their thumbnails in [`../videos/thumbnails`](../videos/thumbnails).

| File | Size | Use |
| --- | --- | --- |
| `avatar.png` | 800×800 | Channel picture. Black hexagon on white; reads in both light and dark mode. |
| `avatar-dark.png` | 800×800 | Alternate on black. The hexagon's outer edge blends into the background, so prefer `avatar.png`. |

Both are built from `langsys-website/static/logo/icon.png`, centred with padding so YouTube's circular crop doesn't clip the hexagon's points.

| `banner.png` | 2560×1440 | Channel banner. Tagline plus "Hello" in seven languages, all inside the centre 1546×423 safe area, so phones and desktop show the same thing. No logo or wordmark: the avatar and channel name sit right below the banner. White background in the logo's colours: near-black `#231F20`, grey `#A7A9AC`. |

## Channel description

```
Langsys puts your app in every language without a translation pipeline. The sentence in your code is the key and the default text: no keys file, no extraction step, no redeploy. New text is translated by grammar-aware AI and goes live in your app automatically.

Tutorials, framework guides and product tours for React, Svelte, Vue, Next.js, Laravel and PHP.

Start free: https://langsys.dev
Docs: https://docs.langsys.dev
```

Still to add:

- `watermark.png`: 150×150, shown in the corner of every video.

## Publishing the videos

Every video is uploaded and set unlisted, so the Learning Center can embed it before it goes public. Titles, descriptions, tags, thumbnails and playlists are done. Each video's `publish` date in `videos.json` is its day; the calendar runs Monday, Wednesday and Friday, from 2026-10-19 to 2026-12-16, with each Short going out the same day as the long video it comes from.

On a publishing day, from this folder:

```
python upload.py --publish --dry-run   # what goes out today
python upload.py --publish             # make it public
```

Anything whose date has passed goes out too, so a missed day catches up on the next run. A playlist goes public with its first public video.

| Command | Does |
| --- | --- |
| `python upload.py --calendar` | Lists every date, with what is published and what is due. |
| `python upload.py --reschedule 2026-11-02` | Moves every date not yet published so the first lands on that day, keeping the gaps. Pick a Monday to keep the Monday/Wednesday/Friday rhythm. |
| `python upload.py --sync` | After editing a title, summary or tags in `videos.json`, pushes the change to YouTube. |
| `python upload.py --launch` | The day langsys.dev opens: swaps "Get started" (the docs quickstart) for "Start free: https://langsys.dev" in every description. |

`managing-translations` and `translating-a-content-block` have no date: they are filmed against translation-manager MR !1 and !2. Once those ship, remove their `hold`, run `python upload.py` to upload them, give them a `publish` date and add their ids to the Learning Center's `videos.ts`.
