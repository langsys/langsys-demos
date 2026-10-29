# Tracking where sign-ups come from

Every langsys.dev link the campaign publishes carries UTM parameters, so when someone signs up we know which platform, and which video or post, brought them. The site keeps them in a cookie on `.langsys.dev` and the app sends them with the sign-up, so a person who arrives from a video and signs up days later is still counted. Each arrival from a tagged link or another website is also recorded on its own (the API's `landings` table), so we see how many people each video or post brings, not only how many sign up.

## The parameters

| Parameter | Says | Values |
|---|---|---|
| `utm_source` | where the link sits | `youtube`, `x`, `linkedin`, `reddit`, `discord`, `devto`, `hashnode`, `alternativeto`, `javascript_weekly`, `frontend_focus`, `svelte_newsletters`, `console_dev` |
| `utm_campaign` | the campaign | `launch_2026` (`utm_campaign` in `youtube/videos.json`) |
| `utm_content` | which video or post | the video's file with `/` as `-` (`svelte-hero`, `react-react-t-string`), the subreddit (`r-sveltejs`), or `launch-thread` / `launch-post` for launch day |

There is no `utm_medium`. The kind of placement always follows from the source (`youtube` is a video, `x` and `linkedin` are social, `reddit` and `discord` are community, and so on), so the API works it out from the source. The list is in langsys-nova's `config/attribution.php`. A visit with no source that came from another website is counted as `referral`. Add `utm_medium` by hand only when a source's usual kind doesn't hold, such as `utm_medium=paid` on an ad. A link that states a medium keeps it.

Values are lowercase, with `_` inside a name and `-` inside a slug. A new platform gets a new `utm_source`; don't reuse one, or its sign-ups are counted as the other's. Add the new source to `config/attribution.php` too, or its visits have no kind of placement.

## Where the tags are

- **YouTube:** `upload.py` adds them to every langsys.dev link in each description, in all 18 languages (`utm.py`). `--sync` and `--launch` push them; nothing changes on YouTube until one of those runs.
- **X and LinkedIn:** each reply or first comment has the YouTube link and, under it, a tagged "Try it free" link. Without it, someone who comes from X watches on YouTube and is counted as YouTube. `social_posts.py` writes new SDK sets the same way.
- **Reddit, the Svelte Discord, AlternativeTo:** the links in each post are tagged for that place.
- **Newsletters:** one text for all four; put in that newsletter's link from the table in `communities-and-listings.md`.
- **Articles:** tagged `devto`. When cross-posting to Hashnode, change `utm_source=devto` to `utm_source=hashnode` in the body. Leave `canonical_url` untagged: it tells search engines which copy is the original.

## Links left untagged, on purpose

- **Hacker News:** HN readers distrust tracking parameters in a Show HN URL. The site records the referrer (`news.ycombinator.com`) instead.
- **Product Hunt:** it adds its own `?ref=producthunt` to outgoing links.
- **MCP directories:** the server URL (`mcp.langsys.dev`) is an endpoint, not a page, and must stay exact. Sign-ups made through an AI assistant are counted as `mcp` by the connection itself; directory visitors who open the docs are counted by referrer.
- **YouTube links** (`youtu.be/...`): parameters there don't reach langsys.dev.

## Posting something by hand

To post a langsys.dev link anywhere not listed here, tag it first:

```
cd youtube
python -c "import utm; print(utm.tag('https://langsys.dev/', 'SOURCE', 'CONTENT'))"
```
