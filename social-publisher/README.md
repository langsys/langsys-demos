# social-publisher

Post text, images and videos to **YouTube**, **X** and **LinkedIn** from one command. The tokens live in a `.env` file.

```bash
social-publish post --to x,linkedin --text "We just shipped plurals #i18n" --media demo.mp4
social-publish post --file examples/launch-day.json --dry-run
social-publish check
```

## Install

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"     # Python 3.11+ (.venv/bin/python on macOS/Linux)
cp .env.example .env                                # then fill in the channels you use
```

## Use it from an assistant (MCP)

The usual way to use it: register the MCP server once, then ask in plain words, e.g. *"post demo.mp4 to YouTube titled 'Plurals in 60 seconds', then share it on X and LinkedIn with the link in the first comment"*.

```bash
claude mcp add social-publisher --scope user -- \
  C:/laragon/www/social-publisher/.venv/Scripts/python.exe -m social_publisher.mcp_server \
  --env C:/laragon/www/social-publisher/.env
```

Any other MCP client can run the same command over stdio. It has three tools:

| Tool | What it does |
|---|---|
| `check_accounts` | Confirms the tokens work and shows which account each channel posts as |
| `preview_post` | Runs every check and returns what each channel would get, with links already tagged. Posts nothing |
| `publish_post` | Posts. Every channel is checked first, and a repeated call posts only where the last one failed |

The tools take the same fields as a post file (see below): shared fields at the top level, plus `youtube`, `x` and `linkedin` for each channel's own text, or a `post_file` to start from. The server tells the assistant to preview first and publish only after you confirm.

- **Media paths must be absolute.**
- **Token changes apply at once.** The `.env` is read again on every call, so updated tokens work without restarting the server.
- **Repeated calls don't double-post.** A post without a post file keeps its results under `~/.social-publisher/results`, set by `SOCIAL_PUBLISHER_STATE`, keyed by the post's content. Calling twice with the same arguments posts once, and `force: true` posts again.
- **Big uploads can time out.** Uploading a large video can outlast the client's tool timeout. In Claude Code, raise `MCP_TOOL_TIMEOUT` (in milliseconds) if that happens. Re-calling is safe, because only the unfinished channels run.

Signing in to get the tokens is still a one-time step on the command line (`auth`, below), because it opens a browser.

## Use it from the command line

```bash
social-publish check         # shows who each channel posts as
```

`python -m social_publisher ...` works too if the `social-publish` script isn't on your PATH.

## Posting

Flags work for one-off posts. A JSON post file gives each channel its own text. Top-level fields are shared by every channel, a channel's own block overrides them, and command-line flags override both:

```json
{
  "to": ["youtube", "x", "linkedin"],
  "media": ["clip.mp4"],
  "youtube":  { "title": "Translate a React app", "text": "Long description…", "privacy": "public" },
  "x":        { "text": "Short and punchy #React", "comment": "Full video: {youtube}" },
  "linkedin": { "text": "The longer story… #i18n", "comment": "Full video: {youtube}" }
}
```

| Field | Channels | Meaning |
|---|---|---|
| `text` | all | The post text. On YouTube it's the description |
| `media` | all | Paths, relative to the post file. YouTube takes one video. X takes up to 4 images, or one GIF or video. LinkedIn takes one video or up to 20 images |
| `title` | YouTube (required), LinkedIn | Video title on YouTube, media title on LinkedIn |
| `comment` | all | A first comment. On X it's a reply to the post |
| `tags`, `privacy`, `publish_at`, `playlist`, `category` | YouTube | `privacy` is `public` (the default), `unlisted` or `private`. `publish_at` schedules the video, e.g. `2026-11-02T15:00:00-05:00` |
| `thumbnail` | YouTube, LinkedIn video | JPEG or PNG. On YouTube it must be 2 MB or less |
| `alt_text` | X, LinkedIn | Alt text for the images, in the same order as `media` (not for videos) |
| `utm` | all | Campaign tags for the links: `{"content": "svelte-hero"}` on top of the `.env` defaults, a full `{"domains": [...], "campaign": "...", "content": "...", "exclude": [...]}`, or `false` to leave the links as written |

**Links between channels.** `{youtube}`, `{x}` and `{linkedin}` in a text or comment become the link of what this run just posted there. Channels always run in the order YouTube → X → LinkedIn, so the X and LinkedIn posts can link the video uploaded a moment before.

**Campaign tags.** With `UTM_DOMAINS` and `UTM_CAMPAIGN` in `.env`, every link to those domains (and their subdomains) gets `utm_source=<channel>&utm_campaign=…`, plus `utm_content` when the post gives one (`"utm": {"content": "svelte-hero"}` or `--utm-content`). Each channel gets its own `utm_source`, so the same post shows up as `x` on X and as `linkedin` on LinkedIn. Hosts in `UTM_EXCLUDE` and links that already carry `utm_source` are left alone. No `utm_medium` is added; write it into a link by hand where you need it. `--no-utm` turns tagging off for a run.

**Re-running is safe.** The results of a post file are kept next to it (`launch.json` → `launch.posted.json`). Running the file again posts only to the channels that failed, and `{youtube}` still links the video the first run uploaded. `--force` posts to every channel again, and `--results` picks a different results file.

**Rate limits and hiccups.** A rate limit of a minute or less is waited out. A longer one fails the channel and says when the limit resets. Server errors and dropped connections are retried up to three times, but only for requests that are safe to repeat: uploads and status checks, never the post itself. A post that times out might still have gone up, so check the channel before you use `--force`.

**Nothing goes half out.** Every channel is checked before anything is posted: tokens present, media types and sizes, text lengths, placeholders. One problem stops the whole run. `--dry-run` runs the checks and prints the plan. If a post went up but a follow-up step failed (thumbnail, playlist, comment), the post counts as ok and the step shows as a warning. Exit codes: `0` all posted, `1` a channel failed, `2` nothing posted. `--json` prints the results as JSON.

## Getting the tokens

### YouTube

1. In Google Cloud, enable **YouTube Data API v3** and create an OAuth client of type **Desktop app**. Download its JSON.
2. `social-publish auth youtube --client-file client.json --write` opens the browser. Sign in, pick the channel, and the three `YOUTUBE_*` values are written to `.env`.
   - If you already have an authorized-user token file (like the one `langsys-demos/youtube` uses), `--token-file` copies its values without signing in.
3. While the consent screen is in **Testing**, Google revokes refresh tokens after 7 days. Set it to **In production** for a token that lasts.

Videos are uploaded private and then switched to the visibility you asked for, because an unaudited API project can't upload any other way. Each upload costs about 1,600 of the default 10,000 daily quota units. Comments need the `youtube.force-ssl` scope, which `auth youtube` asks for.

### X

1. In the X developer portal, set the app's **User authentication settings** to **Read and write**.
2. Then generate the **Access Token and Secret** (tokens generated before that change are read-only). Copy them, along with the API key and secret, into the four `X_*` variables. These OAuth 1.0a tokens don't expire.
3. Posting needs a paid API tier that allows writes. With X Premium, set `X_MAX_CHARS=25000` to allow long posts.

### LinkedIn

1. Create an app at developer.linkedin.com, add the products **Share on LinkedIn** and **Sign In with LinkedIn using OpenID Connect**, and add `http://localhost:8765/callback` as a redirect URL.
2. Put `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET` in `.env`, then run `social-publish auth linkedin --write`. That writes `LINKEDIN_ACCESS_TOKEN` and your `LINKEDIN_AUTHOR` (`urn:li:person:…`).
3. To post as a **company page**, the app needs the Community Management API, which LinkedIn has to approve. Then run `--scopes "w_organization_social r_organization_social"` and set `LINKEDIN_AUTHOR=urn:li:organization:<page id>`.
4. Access tokens last 60 days. Sign in again before they expire (`auth linkedin` prints the date).

`LINKEDIN_VERSION` pins the API version (`YYYYMM`). LinkedIn supports each version for about a year, so bump it when posting starts to fail with a version error.

## Tests

```bash
python -m pytest
```

The tests use fake HTTP sessions and never contact a real channel.
