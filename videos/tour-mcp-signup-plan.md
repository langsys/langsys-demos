# tour-mcp-signup — plan (draft, 2026-10-07)

A new user sets up a Langsys account from Claude Code: sign-in, name,
organization, a paid plan paid in the browser, languages, a first project and an
API key. It's the sign-up companion to `tour-mcp`, which shows an existing
account connecting and reading.

**Status: waiting on deploy.** The flow (`account_status`, `wait_for_plan`, the
setup guidance) exists only on `docs` branch `feature/mcp-local-setup` (6 commits,
2026-10-06/07). Production `mcp.langsys.dev` lists 214 tools and neither of
those. We film against production once it ships. **Before filming, re-read
`setupSteps()` / `setupStepGuidance()` on whatever was deployed:** the beats
below follow the branch as of a127aab and will drift if the flow changes.

Decisions (user, 2026-10-07): film after deploy · Claude Code terminal cards,
like `tour-mcp` · **paid plan, payment shown** · a fresh email the user provides.

## How it is filmed

Same harness as `tour-mcp` (`record_tour.py`, `narrate_tour.py`):

- Terminal half: **real** Claude Code output, rendered as terminal cards,
  verbatim, with tool calls in the tool colour. A conversation has several
  turns, so it can't be one `claude -p` like `tour-mcp`. Each turn is
  `claude -p --resume <session>` with the scripted user reply, through an
  `--mcp-config` file and `--strict-mcp-config`, as before.
- Browser half: the recorded browser follows the real sign-in, consent and
  payment pages.
- The payment turn blocks inside `wait_for_plan` (up to 30 min). The harness
  starts that turn in the background, records the payment in the browser, then
  collects the turn's output once it returns settled.
- Without `--go`, a take reuses the saved transcript (`out/mcp-signup-run/`),
  so re-shooting the picture doesn't create another account or pay again.

## Beats and narration

| # | Beat | Picture | Narration (draft) |
|---|---|---|---|
| 1 | one command | terminal card: `claude mcp add --transport http langsys https://mcp.langsys.dev/mcp` + its output | You can start using Langsys without ever opening a sign-up form: just connect your AI assistant. |
| 2 | first message | user types "Hi! I'd like to translate my app with Langsys." | Say hello, and it takes it from there. |
| 3 | sign in | browser opens on Langsys's sign-in page; email, code from inbox (or passkey) | Signing in happens on Langsys's own page, with a passkey or an emailed code, so the assistant never sees a password. |
| 4 | approve | Authorize Access screen → approve → "Connected" | Approve the connection, and you're back in the conversation. |
| 5 | it knows where you are | `account_status` call; assistant asks the user's name | It checks the account first, so it knows exactly what's left to set up, and asks one thing at a time. |
| 6 | name + organization | user gives name, then org name; two PATCH calls | Your name, then what to call your organization. |
| 7 | the plans | assistant lists plans with prices; user picks a paid plan; asked monthly or yearly with the yearly saving | Next it shows the plans with real prices, and when you pick one, asks monthly or yearly, and what yearly saves you. |
| 8 | the payment page | assistant opens the payment page itself; "Take your time, I'll wait here while you pay" | Payment never happens in chat. It opens the payment page for you, and waits. |
| 9 | pay | browser: the plan's payment step, card entered, paid, "go back to your assistant" | You pay on Langsys, like you would anywhere else. |
| 10 | it carries on | terminal: `wait_for_plan` returns settled; plan confirmed; asks languages | And the moment it goes through, the assistant carries on by itself, with nothing to tell it. |
| 11 | languages | user: "English, into Spanish, French and Japanese"; settings saved | Tell it your app's language and the ones you want, |
| 12 | first project | user gives app name + URL; project created | name your first project, |
| 13 | API key | write key created, shown once, read from `LANGSYS_API_KEY` | and it creates an API key for development, shows it once, and tells you to keep it in an environment variable. |
| 14 | the same account | browser: dashboard with the new org, plan and project | Open the dashboard, and it's all there, exactly as if you'd clicked through it yourself. |
| 15 | close | — | One conversation, from nothing to a project ready for your app. |

Title card: **Set up Langsys from your AI assistant** / sub: *Account, plan,
languages and a first project, without leaving the conversation.*
Outro card: same pattern as `outrocard-mcp.html`.

Claim only what's on screen (see agent-first positioning). The SDK install
(`npx langsys-skill install`) is offered at the end of the flow, but it isn't
filmed here, so the narration doesn't promise it.

## Open before filming

1. **Payment on production.** A paid plan on prod charges a real card. Decide:
   real card + refund/cancel afterwards, a 100%-off coupon if checkout accepts
   one, or a test-mode path, if production has one. Ask the teammate.
2. **Email.** The user provides a fresh inbox; the take reads the code from it
   (by hand, or a passkey on this machine).
3. **Cleanup.** Each `--go` take creates a real organization and subscription.
   Note how to delete or cancel it afterwards.
4. **Re-check the flow after deploy**: situations, the wording of the
   payment-link step, and whether sign-up of a brand-new email goes through the
   consent page or a separate sign-up page first.
