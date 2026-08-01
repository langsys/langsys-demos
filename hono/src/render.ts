import type { ServerTFunction } from 'langsys-js-hono';
import { LOCALES } from './langsys.config.js';

/**
 * The demo page: every example on docs.langsys.dev/learn/sdk pages running
 * live, translated on the server â€” view source: the HTML arrives already
 * localized. Mirrors the Laravel/Symfony demo page (same phrases, same
 * categories) so the whole set translates from the shared demo catalog.
 */
export interface RenderInput {
    t: ServerTFunction;
    locale: string;
    count: number;
    banner: 'shared' | 'unconfigured' | null;
    framework: string;
    docsPath: string;
}

const esc = (value: string): string =>
    value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function bannerHtml(banner: RenderInput['banner']): string {
    if (!banner) return '';
    const message =
        banner === 'shared'
            ? `<strong>Shared demo project (read-only)</strong> â€” existing phrases translate; new or edited ones
               won't. Drop your own keys in <code>.env</code> to watch discovery register and translate your
               phrases live.`
            : `<strong>No Langsys credentials configured</strong> â€” showing source text only, nothing translates.
               Add your project id and key in <code>.env</code> to see it live.`;
    return `<div class="demo-banner" translate="no">${message}
        <a href="https://docs.langsys.dev/learn/concepts/keys-and-environments" target="_blank"
            rel="noopener noreferrer">Get your keys â†’</a></div>`;
}

export function renderDemo({ t, locale, count, banner, framework, docsPath }: RenderInput): string {
    const pills = Object.entries(LOCALES)
        .map(
            ([code, label]) =>
                `<a class="pill${code === locale ? ' active' : ''}"
                    href="?locale=${encodeURIComponent(code)}&count=${count}">${label}</a>`
        )
        .join('\n');

    // t() works anywhere on the server â€” computed here like a controller
    // would, not inline in the template. The date is pre-formatted for the
    // request locale; the order id is a string, so it stays unformatted.
    const orderTitle = t('Order confirmed', 'Checkout');
    const orderBody = t('Your order {id} ships on {date}.', 'Checkout', {
        id: '48213',
        date: new Intl.DateTimeFormat(locale, { dateStyle: 'long' }).format(new Date(2026, 7, 15)),
    });

    return `<!doctype html>
<html lang="${esc(locale)}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Langsys Ã— ${esc(framework)} â€” demo</title>
    <link rel="stylesheet" href="/demo.css">
</head>
<body>
    ${bannerHtml(banner)}
    <div class="app">
        <header class="topbar">
            <div class="brand"><span class="logo">â—†</span> <span translate="no">Langsys</span> Ã— ${esc(framework)}</div>
            <!-- Server-rendered locale switcher: plain links. The middleware
                 picks up ?locale= and persists it (cookie), so navigation keeps it. -->
            <nav class="locales" translate="no">${pills}</nav>
        </header>

        <section class="card">
            <h2><code>t()</code> â€” inline string</h2>
            <div class="live">
                <p>${t('Hello, {name}!', 'Greetings', { name: 'Sarah' })}</p>
            </div>
        </section>

        <section class="card">
            <h2><code>t()</code> â€” ICU plurals, from the interactive playground</h2>
            <div class="live">
                <p>${t('Hello, {name}! You have {count, plural, one {# new message} other {# new messages}}.', 'Greetings', { name: 'Sarah', count })}</p>
                <div class="stepper" translate="no">
                    <a aria-label="Fewer" href="?locale=${encodeURIComponent(locale)}&count=${Math.max(0, count - 1)}">âˆ’</a>
                    <span class="count">${count}</span>
                    <a aria-label="More" href="?locale=${encodeURIComponent(locale)}&count=${count + 1}">+</a>
                </div>
            </div>
            <p class="hint">
                Change count to 1 and back â€” the grammar follows. Every locale applies its own plural rules,
                resolved server-side by ICU.
            </p>
        </section>

        <section class="card">
            <h2><code>t()</code> â€” anywhere on the server</h2>
            <div class="live">
                <p>${orderTitle}</p>
                <p>${orderBody}</p>
            </div>
            <p class="hint">
                Computed in the handler â€” the same function works in services, jobs, and mailers. The date is
                locale-formatted; the order id is a string, so it stays unformatted.
            </p>
        </section>

        <section class="card">
            <h2>Categories â€” same phrase, different meaning</h2>
            <div class="live">
                <p><strong>${t('Home', 'Main Menu')}</strong> Â· <strong>${t('Home', 'Home repairs')}</strong></p>
            </div>
            <p class="hint">
                The category scopes the phrase, so the same words translate differently per context â€” in Spanish,
                "Inicio" for the menu entry and "Hogar" for the service.
            </p>
        </section>

        <section class="card">
            <h2>Explicit coverage â€” untagged text never translates</h2>
            <div class="live">
                <p>${t('Welcome!', 'Tour')} This sentence always stays in English. ${t('Thanks for visiting!', 'Tour')}</p>
            </div>
            <p class="hint">
                Coverage is explicit: only strings passed through <code>t()</code> are translated. The middle
                sentence is untagged, so it passes through verbatim â€” no opt-out marker needed.
            </p>
        </section>

        <footer class="meta" translate="no">
            locale: ${esc(locale)} Â· server-rendered Â·
            <a href="https://docs.langsys.dev/${docsPath}" target="_blank" rel="noopener noreferrer">
                How this works â†—
            </a>
        </footer>
    </div>
</body>
</html>`;
}

