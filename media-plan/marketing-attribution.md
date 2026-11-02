# Langsys marketing attribution

> Markdown copy of the [marketing attribution page](https://claude.ai/artifact/4Hve8CqxJwnuiyoANggeLE), 2026-10-29. The engineering details are in langsys-nova `docs/signup-attribution.md`; the tagging rules are in `launch/tracking.md`. Ticket 986.

Every link we share for the launch carries a small label. When someone visits the website or creates an account, we can see which platform and which video or post brought them.

## What it lets us answer

- **Which video brought the most visitors?** Counted per platform, campaign and individual post.
- **Which post actually turned into accounts?** Real sign-ups, not just clicks.
- **How many visitors from X end up signing up?** Visits and sign-ups are linked, so we can compare them.

## How it works

1. **We label every link.** Each link we post records where it was posted (YouTube, X, LinkedIn, Reddit, a newsletter) and which video or post it belongs to.
2. **The website remembers.** When someone arrives, the site keeps a note of where they came from for 90 days.
3. **We count the visit.** Every arrival from a labelled link, or from another website, is recorded.
4. **The account keeps it.** If they sign up, even days later, the new account records how they found us.

## What a labelled link looks like

The label is a few extra words at the end of an ordinary link. The page opens exactly the same, and the visitor doesn't need to do anything.

```
https://langsys.dev/?utm_source=youtube&utm_campaign=launch_2026&utm_content=svelte-hero
```

| Part | Says | Here |
|---|---|---|
| `utm_source` | where the link was posted | YouTube |
| `utm_campaign` | which campaign | the 2026 launch |
| `utm_content` | which exact post | the Svelte video |

Nobody types these by hand. A small tool adds them to every link in our YouTube descriptions and social posts, in all 18 languages.

**The kind of post is worked out for us.** YouTube is always a video, X and LinkedIn are always social, and Reddit is always a community, so the link doesn't need to say it. Langsys fills it in from the source. A link spells it out (`utm_medium=…`) only when the usual kind doesn't apply, for example a paid ad on LinkedIn.

## Platforms

| Platform | Where the link sits | Counted as | Labelled by | Link |
|---|---|---|---|---|
| YouTube | Video description, in all 18 languages | video | Tool, automatically | `langsys.dev/?utm_source=youtube&utm_campaign=launch_2026&utm_content=svelte-hero` |
| X | "Try it free" in the reply under each post | social | Tool, automatically | `langsys.dev/?utm_source=x&utm_campaign=launch_2026&utm_content=launch-thread` |
| LinkedIn | "Try it free" in the first comment | social | Tool, automatically | `langsys.dev/?utm_source=linkedin&utm_campaign=launch_2026&utm_content=adding-a-language` |
| Reddit | Body of the post, one per subreddit | community | Written into the post | `docs.langsys.dev/learn?utm_source=reddit&utm_campaign=launch_2026&utm_content=r-sveltejs` |
| Discord | Message in the Svelte server | community | Written into the post | `docs.langsys.dev/learn?utm_source=discord&utm_campaign=launch_2026&utm_content=svelte-discord` |
| Dev.to | Links inside the article | article | Written into the article | `docs.langsys.dev/learn?utm_source=devto&utm_campaign=launch_2026&utm_content=plurals-and-gender` |
| Hashnode | Same article, cross-posted | article | By hand: change `devto` to `hashnode` | `docs.langsys.dev/learn?utm_source=hashnode&utm_campaign=launch_2026&utm_content=plurals-and-gender` |
| Newsletters | The blurb we submit (JavaScript Weekly, Frontend Focus, Svelte newsletters, Console.dev) | newsletter | Written into the blurb, one link per newsletter | `langsys.dev/?utm_source=javascript_weekly&utm_campaign=launch_2026&utm_content=launch-blurb` |
| AlternativeTo | Website field of our listing | listing | Written into the listing | `langsys.dev?utm_source=alternativeto&utm_campaign=launch_2026&utm_content=alternativeto` |
| Product Hunt | The launch page | listing | Product Hunt adds its own `?ref=` | `langsys.dev/?ref=producthunt` |
| Hacker News | The Show HN post | referral | Left plain on purpose | `langsys.dev/` (known from the visitor's previous site) |
| AI assistant | When someone connects Claude, Cursor or another assistant | assistant | Langsys, automatically | `…?utm_source=mcp` |

X and LinkedIn posts carry their own link because of how the counting works. If they only pointed to YouTube, a person who came from X would watch on YouTube and be counted as YouTube.

## What happens on our end

1. **The page reads the label.** When a page on langsys.dev, the docs or the app opens, a small script looks at the link. It counts the visit only if the link has a label, or if the person came from another website. These don't count:
   - moving between our own pages
   - opening a page directly
   - clicking the sign-in email from Gmail or Outlook
2. **The browser keeps two notes.** The *first* note records what first brought the person to Langsys and is never overwritten. The *last* note is replaced on every new counted visit. Both sit in a cookie shared by all our sites, together with a random visitor number.
3. **The visit is sent to Langsys.** The script sends the visit in the background: the label, the site they came from, the page they landed on and the visitor number. The page never waits for it, and if it fails, nobody notices.
4. **Langsys checks and stores it.** Anything malformed or oversized is refused, and one address can send at most 10 visits a minute, so nobody can flood the numbers. The visit is saved, and its category (video, social, newsletter…) is filled in from the platform.
5. **The sign-up carries the notes.** When someone types their email to sign up, the app sends both notes and the visitor number with it. Langsys keeps them with the pending sign-in until the code or link is used, which is why opening the email on another device still works.
6. **The account keeps them.** When the new account is created, its first and last visit are saved with it. An existing customer signing in again changes nothing, because attribution describes how an account was won.
7. **The report joins it up.** Visits and accounts share the visitor number, so we can count, per platform and post, how many people arrived and how many of them signed up.

## The script that reads the link

A small script of about 60 lines runs first thing on every page of our sites, before anything else loads. It:

- **reads the label** from the link the visitor arrived with, or notes the website they came from
- **decides whether the visit counts**, ignoring visits between our own pages, direct visits, and the sign-in email opened from webmail
- **writes the notes** into the shared cookie: the first visit (kept), the last visit (updated) and the random visitor number
- **sends the visit to Langsys** in the background; if anything goes wrong it stays silent, so it can never break the page

It lives in three repositories, all on the `feature/986_signup_attribution_capture` branch:

| Repository | File | Website |
|---|---|---|
| docs (the original) | `src/lib/attribution-boot.js`, loaded by `src/components/ThemeProvider.astro` and `src/learn/layouts/Base.astro` | docs.langsys.dev and the Learning Center |
| langsys-website | `src/app.html` (a copy, pasted in) | langsys.dev |
| translation-manager | `src/app.html` (a copy, pasted in); `src/lib/js/attribution.ts` reads the notes at sign-up and sends them | app.langsys.dev |
| langsys-nova | no script: the API that stores visits and saves the source with each new account | api.langsys.dev |

The two copies must stay identical to the original, so a change to the script is made in all three repositories.

## How we recognise a returning visitor

We don't use IP addresses. The browser remembers the visitor for us, with a cookie.

- **First visit:** the site gives the browser a random visitor number and notes the label of the link they came from.
- **Coming back:** days later, even without a link, the same browser still has the number and the note, for up to 90 days.
- **Signing up:** the app sends the number and the notes with the sign-up, so the new account is tied to every earlier visit.

**Why not IP addresses?**
- One IP is often shared by a whole office, café or mobile network.
- The same person's IP changes between home Wi-Fi and their phone.
- An IP address is personal data under GDPR. A random number that only means something to us is not.

**In practice,** the cookie knows the browser, not the person. A visit on a phone followed by a sign-up on a laptop shows up as two different visitors, unless the sign-in email itself connects them.

## An example

Ana watches our Svelte video on YouTube and clicks the link in the description. She reads the docs, then leaves. A week later she sees a LinkedIn post, comes back and creates an account.

We record both visits. Her account shows that YouTube introduced her to Langsys and that LinkedIn brought her back to sign up, so both posts get credit for their part.

## A few things worth knowing

- **First and last visit:** we keep the visit that introduced someone to Langsys and the one that finally brought them back to sign up.
- **AI assistants count too:** someone who connects Langsys through Claude, Cursor or another assistant is counted as coming from an AI assistant.
- **Some links stay unlabelled on purpose:** Hacker News readers dislike tracking labels, so that link stays plain. We still see the visit came from Hacker News. Product Hunt adds its own label.
- **Opening the sign-in email on another device still works:** where someone came from travels with the email, not just the browser.

## What it can't see

It misses:
- people who block cookies
- someone who visits on their phone and later signs up on their laptop (only the laptop's visits count)
- visits older than 90 days
- links shared in private messages or apps that hide where the visitor came from (these look like direct visits)

The numbers are a reliable guide to which platforms and posts work best. They are not an exact count of every person.

## Privacy

Everything stays with us. We store:
- a random visitor number
- the link's label
- the website the person came from
- the page they landed on

We store no names until someone signs up, and we share nothing with advertisers or other companies. The privacy policy on the website describes this.

**Still open:**
- a legal review of the privacy policy wording
- whether visitors in the EU must agree before we keep these notes

## Where it stands

- **Built:** labelled links, visit counting on the websites, and sign-ups that record their source. The code is pushed and waiting for review before it goes live.
- **Next:** a report in the admin panel showing visitors and sign-ups by platform, campaign and post, and how many become paying customers.
- **To decide:** the privacy questions above.
