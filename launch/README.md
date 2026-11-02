# Launch kit

Everything for launch outside YouTube's own uploads, ready to paste. Days are counted from launch Monday ("launch + N"), like the rest of the calendar; launch is Monday 26 October 2026, and each day carries its date.

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

- [x] **Set the launch date:** Monday 26 October 2026.
- [ ] **LinkedIn company page:** create it if it doesn't exist, and decide who posts from it.
- [ ] **Hacker News and Product Hunt accounts** for the founder who will post. Product Hunt: profile filled in at least a week before; schedule the launch for launch + 8 · Tue 3 Nov 2026.
- [ ] **dev.to and Hashnode accounts** (or just dev.to) for the articles.
- [ ] **Reddit account** with some history; check each community's self-promotion rules.
- [ ] **DNS:** add the TXT record `mcp-publisher` prints for langsys.dev, so the server can be listed in the official MCP Registry as `dev.langsys/langsys`.
- [ ] **GitHub:** fork awesome-mcp-servers for the pull request (any account works).
- [ ] **Fill in `[name]`** in the Show HN text and the Product Hunt maker comment.
- [ ] **Check pricing** on langsys.dev/pricing against what these drafts say about the free plan.

## Launch week, day by day

**Launch day · Mon 26 Oct 2026**

1. `python upload.py --launch`, then `--publish` (see the runbook in the Launch Media Plan): the 9 starting videos go public.
2. X: post the launch thread and pin it.
3. LinkedIn: post the launch post with the explainer; the links go in the first comment.
4. MCP directories: publish to the official registry, then submit to Smithery and mcp.so, and open the awesome-mcp-servers pull request.
5. Listings: submit AlternativeTo and G2.
6. Newsletters: send the four submissions.

**Launch + 1 · Tue 27 Oct 2026**

1. Hacker News: post Show HN between 8 and 10 a.m. US Eastern, and stay in the comments all day.
2. X and LinkedIn: the day's Short.

**Launch + 2 · Wed 28 Oct 2026**

1. Reddit r/sveltejs, the Svelte Discord showcase, and the Svelte Society submission: all with the Svelte walkthrough, which goes public that day.
2. X and LinkedIn: the day's video.

**Launch + 3 and + 4 · Thu 29 and Fri 30 Oct 2026:** the day's X and LinkedIn posts only.

**Week 2 onwards**

- **Launch + 8 · Tue 3 Nov 2026:** Product Hunt goes live at 00:01 Pacific. Post the maker comment at once, and mention it on X and LinkedIn mid-morning.
- **Week 2:** publish article 1 (`articles/01-the-sentence-is-the-key.md`).
- **Launch + 14 · Mon 9 Nov 2026:** Reddit r/SaaS.
- **Week 3 or 4:** publish article 2 (`articles/02-plurals-and-gender.md`).
- **Launch + 35 · Mon 30 Nov 2026:** Reddit r/webdev.
- **A week after launch:** check that Langsys shows up on PulseMCP and Glama; submit by hand if not.

Every weekday through week 8: `python upload.py --publish`, then that day's X and LinkedIn posts.
