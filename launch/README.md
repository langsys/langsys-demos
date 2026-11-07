# Launch kit

Everything for launch outside YouTube's own uploads, ready to paste. Days are counted from launch Monday ("launch + N"), like the rest of the calendar; launch is Monday 9 November 2026, and each day carries its date.

| File | What's in it |
|---|---|
| `../x/posts.md` | The X launch thread and one post per publishing day |
| `../linkedin/posts.md` | The LinkedIn launch post and one post per publishing day |
| `hacker-news.md` | The Show HN title, text, and answers to the questions every i18n launch gets |
| `product-hunt.md` | Tagline, description, maker comment, gallery order |
| `product-hunt/` | Thumbnail (240×240) and six gallery images (1270×760) |
| `mcp-directories.md` | Listings for the official MCP Registry (with `server.json`), Smithery, mcp.so and awesome-mcp-servers |
| `reddit.md` | Three posts: r/sveltejs, r/SaaS, r/webdev |
| `communities-and-listings.md` | Svelte Discord, Svelte Society, newsletters, AlternativeTo, G2, Bluesky and Mastodon |
| `articles/` | Two dev.to and Hashnode articles, ready to publish |
| `tracking.md` | The UTM tags on every langsys.dev link, so each sign-up shows which platform and post it came from |

## What only you can do, before launch

None of these can be done from the repository; each needs an account, a login or a decision.

- [x] **Set the launch date:** Monday 9 November 2026.
- [ ] **LinkedIn company page:** create it if it doesn't exist, and decide who posts from it. Needed by week 3 (Mon 23 Nov 2026), not launch day.
- [ ] **Hacker News and Product Hunt accounts** for the founder who will post. Product Hunt: profile filled in at least a week before; schedule the launch for launch + 22 · Tue 1 Dec 2026.
- [ ] **dev.to and Hashnode accounts** (or just dev.to) for the articles.
- [ ] **Reddit account** with some history; check each community's self-promotion rules.
- [ ] **DNS:** add the TXT record `mcp-publisher` prints for langsys.dev, so the server can be listed in the official MCP Registry as `dev.langsys/langsys`.
- [ ] **GitHub:** fork awesome-mcp-servers for the pull request (any account works).
- [ ] **Fill in `[name]`** in the Show HN text and the Product Hunt maker comment.
- [ ] **Check pricing** on langsys.dev/pricing against what these drafts say about the free plan.

## Launch, in two phases

**Weeks 1 and 2 (Mon 9 to Fri 20 Nov 2026): YouTube and X only.** Sign-up, attribution and the posts are tried on a smaller audience first, so anything broken is fixed before the one-shot launches (Hacker News and Product Hunt can only be done once).

**From week 3 (Mon 23 Nov 2026): LinkedIn and everything else**, once the first two weeks show sign-up and the counts working.

**Launch day · Mon 9 Nov 2026**

1. `python upload.py --launch`, then `--publish` (see the runbook in the Launch Media Plan): the 9 starting videos go public.
2. X: post the launch thread and pin it.

**Every publishing day in weeks 1 and 2:** `python upload.py --publish`, then that day's X post. No LinkedIn, no communities. At the end of week 2, check in the attribution report that sign-ups from `utm_source=x` and `youtube` are being counted.

**Launch + 14 · Mon 23 Nov 2026 (week 3 starts)**

1. LinkedIn: post the launch post with the explainer; the links go in the first comment. From here on, that day's LinkedIn post on every publishing day, as `../linkedin/posts.md` dates it.
2. MCP directories: publish to the official registry, then submit to Smithery and mcp.so, and open the awesome-mcp-servers pull request.
3. Listings: submit AlternativeTo and G2.
4. Newsletters: send the four submissions.

**Launch + 15 · Tue 24 Nov 2026**

1. Hacker News: post Show HN between 8 and 10 a.m. US Eastern, and stay in the comments all day.
2. LinkedIn: the Add German post (moved from Monday, which carries the launch post).

**Launch + 16 · Wed 25 Nov 2026**

1. Reddit r/sveltejs, the Svelte Discord showcase, and the Svelte Society submission: all with the Svelte walkthrough (public since week 1, Wednesday).
2. Publish article 1 (`articles/01-the-sentence-is-the-key.md`).

Thursday 26 November is Thanksgiving in the US: nothing new outside the calendar's own X and LinkedIn posts on Thursday and Friday.

**Week 4 onwards**

- **Launch + 21 · Mon 30 Nov 2026:** Reddit r/SaaS.
- **Launch + 22 · Tue 1 Dec 2026:** Product Hunt goes live at 00:01 Pacific. Post the maker comment at once, and mention it on X and LinkedIn mid-morning.
- **Week 5:** publish article 2 (`articles/02-plurals-and-gender.md`).
- **Launch + 35 · Mon 14 Dec 2026:** Reddit r/webdev.
- **A week after the MCP listings (Mon 30 Nov 2026):** check that Langsys shows up on PulseMCP and Glama; submit by hand if not.

Every publishing day through the end of the calendar: `python upload.py --publish`, then that day's X post, and from week 3 its LinkedIn post.
