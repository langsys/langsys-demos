# Show HN

**When:** launch + 1 · Tue 27 Oct 2026 (Tuesday), between 8 and 10 a.m. US Eastern.
**Who:** a founder, from a personal Hacker News account (not a brand account). Hacker News readers expect to talk to the person who built it.
**Rules that matter:** the title starts with "Show HN:", the product must be usable without talking to sales (the Free plan is), and no one may be asked to upvote. A post that is asked for votes gets flagged.

## Title (80 characters max)

```
Show HN: Langsys – i18n where the sentence is the key, no keys file or redeploy
```

Fallback if a shorter one reads better:

```
Show HN: Langsys – translate your app at runtime, no keys file
```

## URL

`https://langsys.dev`

## Text (goes in the text box; Hacker News allows a URL and text together)

```
Hi HN, I'm [name], one of the people building Langsys.

Every i18n setup I've worked with has the same loop: invent a key, add it to a JSON file, extract, send the file to translators, import it back, ship a release. Every new sentence starts the loop again, and the keys file drifts from the code.

Langsys removes the loop. The sentence in your code is the key:

    t('Your cart is empty', 'Cart')

The first time that line runs, the SDK registers the phrase with Langsys. It's machine-translated on arrival (or waits for a person, your choice per project), and a translator or the person who owns the copy can review it in a web Translation Manager. Corrections reach the running app without a deploy.

Some details that took the most work:

- Plurals and gender use ICU. You write one sentence; Langsys generates the plural branches each language needs (Russian has four, Arabic six) and the gender branches for languages that agree with the person.
- A sentence with markup inside (a bold word, a link) stays one phrase, so the translator sees the whole sentence and the bold lands where that language puts it.
- Brand names can be held back inline, and the same English word with two meanings ("Free" as a price vs. a free evening) is split by a category instead of an invented key.
- Translation memory is shared across an organization's projects, so a new project starts already translated and no model is called for it.
- There's a hosted MCP server (https://mcp.langsys.dev), so Claude Code, Cursor, Codex or Copilot can see which languages are behind and translate what's missing. Sign-in is an OAuth approval in the browser; the assistant never sees a password, and billing can't be reached from it.

SDKs are open source (MIT): TypeScript, React, Vue and Svelte on npm, and PHP, Laravel and Symfony on Packagist. More frameworks are in progress.

There's a free plan (one project, AI translation words included on signup). Machine translation beyond that is billed per source word, quoted before anything runs.

A 77-second overview: https://youtu.be/q_a37CzxWrk
Docs and the Learning Center: https://docs.langsys.dev/learn

I'd love feedback, especially from anyone who has maintained a keys file in a large app, and on where this approach breaks down for you.
```

Before posting: check the free-plan words and the SDK list against langsys.dev/pricing and npm on the day, and replace `[name]`.

## Answers to have ready

These questions come up on every i18n launch. Short, honest answers work best; link to the docs rather than pasting them.

**"What happens when I change the English sentence? Doesn't that break every translation?"**
The new sentence registers as a new phrase and is translated like any other (drafted on arrival, or queued for a person). That's by design: the sentence is what the translator translated, so a changed sentence deserves a fresh look. If the same sentence exists anywhere in your organization, translation memory fills it in without calling a model.

**"Isn't the sentence a bad key? What about the same word with two meanings?"**
That's what the category argument is for: `t('Free', 'Pricing')` and `t('Free', 'Calendar')` are two phrases. The video: https://youtu.be/-P963Wj0dno

**"What about performance? Is every string a network call?"**
No. The SDK loads the locale's catalog and translates from it; only phrases the catalog doesn't have yet are registered. Server frameworks (Next.js, Nuxt, SvelteKit) seed the catalog on the server.

**"What if Langsys is down?"**
The source-language sentence is in your code, so the app still renders, in the source language. The SDK doesn't queue registrations while it can't reach Langsys, so nothing piles up and floods in when it comes back.

**"Can I export my translations? Vendor lock-in?"**
Everything is reachable through the public API (the same one the MCP server exposes), so translations can be read out at any time.

**"Why not just use i18next / Lokalise / Crowdin?"**
Those are good tools built around the keys file and the export/import loop. Langsys is for teams that want to drop that loop: no keys, phrases register at runtime, and fixes go live without a release.

**"Is the machine translation any good?"**
It's a draft. Projects choose whether drafts go live automatically or wait for review, and every human correction goes into translation memory.

**"Self-hosting?"**
Answer honestly with the current plan; don't promise a date.
