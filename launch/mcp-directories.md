# MCP directories

Listings for the hosted MCP server, so someone searching for a translation or localization MCP server finds Langsys. Submit them on launch day: a listing is public as soon as it's accepted.

The facts every listing uses:

- **Server URL:** `https://mcp.langsys.dev` (remote, Streamable HTTP; the older `https://mcp.langsys.dev/mcp` keeps working)
- **Auth:** OAuth 2.1 with dynamic client registration and PKCE. The client opens a browser to sign in at app.langsys.dev; there's no API key to paste.
- **Docs:** `https://docs.langsys.dev/guides/mcp`
- **Video:** `https://youtu.be/KafvNJnm-pQ`

## Shared copy

**Name:** Langsys

**One line (under 100 characters):**

```
Translation management for your app: see which languages are behind and translate what's missing.
```

**Description:**

```
Langsys is a translation management platform for web and mobile apps. Its MCP server lets your AI assistant work in your Langsys account: check which languages are behind, read and edit translations, machine-translate what's missing, manage projects, languages and API keys, and set up a new project end to end.

Sign-in is an OAuth approval in your browser, so the assistant never sees a password. Billing, payment methods and account deletion stay in the app and can't be reached from the assistant.

The server also exposes the full Langsys API reference as resources, and a setup prompt that walks a new account from sign-up to a translated app.
```

**Tags / categories:** translation, localization, i18n, developer tools, productivity

**Install snippets:**

Claude Code:

```bash
claude mcp add --transport http --scope user langsys https://mcp.langsys.dev
```

Claude Desktop, Cursor, Windsurf and other clients:

```json
{
  "mcpServers": {
    "langsys": {
      "type": "http",
      "url": "https://mcp.langsys.dev"
    }
  }
}
```

## 1. Official MCP Registry (registry.modelcontextprotocol.io)

Published with the `mcp-publisher` command-line tool. A remote server's name is namespaced by a domain you prove you own, so `dev.langsys/langsys` needs a DNS TXT record on langsys.dev.

1. Install `mcp-publisher` (see the registry's README on GitHub: modelcontextprotocol/registry).
2. In an empty folder, run `mcp-publisher init`, then replace the generated `server.json` with the one below. Keep the `$schema` line `init` generated if it differs; it names the current schema version.
3. `mcp-publisher login dns --domain langsys.dev --private-key <key>`: the tool prints the TXT record to add to langsys.dev's DNS.
4. `mcp-publisher publish`.

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json",
  "name": "dev.langsys/langsys",
  "title": "Langsys",
  "description": "Translation management for your app: see which languages are behind and translate what's missing.",
  "websiteUrl": "https://docs.langsys.dev/guides/mcp",
  "version": "1.0.0",
  "remotes": [
    {
      "type": "streamable-http",
      "url": "https://mcp.langsys.dev"
    }
  ]
}
```

Several other directories import from this registry, so it goes first.

## 2. Smithery (smithery.ai)

Sign in with GitHub, choose to add a server, and pick the option for a hosted (remote) server by URL. Use the URL, name, one-line description and description above; add the docs link and the video.

## 3. mcp.so

Submit from the site's "Submit" page: name, server URL, the one line, the description, and `https://docs.langsys.dev/guides/mcp` as the homepage.

## 4. awesome-mcp-servers (github.com/punkpeye/awesome-mcp-servers)

A pull request that adds one line to the README, in the section that fits best (look for a translation, language or developer tools section), keeping the list's alphabetical order and its legend icons (☁️ for a cloud service):

```markdown
- [Langsys](https://docs.langsys.dev/guides/mcp) ☁️ - Translation management for your app: check which languages are behind, edit translations and machine-translate what's missing, with OAuth sign-in.
```

Pull request title: `Add Langsys (translation management)`.

Read the repository's CONTRIBUTING notes on the day; the legend and the section names change from time to time.

## Also worth a listing

PulseMCP (pulsemcp.com) and Glama (glama.ai/mcp/servers) pick servers up from the official registry and GitHub; check a week after launch that Langsys appears, and submit it by hand if not.
