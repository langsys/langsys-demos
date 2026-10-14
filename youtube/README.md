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
