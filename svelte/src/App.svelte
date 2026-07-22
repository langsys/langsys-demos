<script>
    // The Svelte demo app: every example on docs.langsys.dev/learn/sdk/svelte
    // running live, wired by the exact code the docs page shows.
    import { DontTranslate, Phrase, Translate, currentlyLoadedLocale, t } from 'langsys-js-svelte';
    import { LOCALES, LOCALE_LABELS, demoBanner, locale } from './langsys';

    const KEYS_URL = 'https://docs.langsys.dev/learn/concepts/keys-and-environments';
    const DOCS_URL = 'https://docs.langsys.dev/learn/sdk/svelte';

    const name = 'Sarah';
    let messages = $state(3);
    let items = $state(3);
</script>

{#if demoBanner}
    <div class="demo-banner" translate="no">
        {#if demoBanner === 'shared'}
            <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones won't.
            Drop your own keys in <code>.env</code> to watch discovery register and translate your phrases live.
        {:else}
            <strong>No Langsys credentials configured</strong> — showing source text only, nothing translates. Add
            your project id and key in <code>.env</code> to see it live.
        {/if}
        <a href={KEYS_URL} target="_blank" rel="noopener noreferrer">Get your keys →</a>
    </div>
{/if}

<div class="app">
    <header class="topbar">
        <div class="brand"><span class="logo">◆</span> <span translate="no">Langsys</span> × Svelte</div>
        <nav class="locales" translate="no">
            {#each LOCALES as code}
                <button
                    class={($currentlyLoadedLocale || 'en-US') === code ? 'pill active' : 'pill'}
                    onclick={() => locale.set(code)}
                >
                    {LOCALE_LABELS[code] ?? code}
                </button>
            {/each}
        </nav>
    </header>

    <!-- t() — inline string: the $t store re-reads on locale/catalog change. -->
    <section class="card">
        <h2><code>t()</code> — inline string, in a component</h2>
        <p class="live">{$t('Hello, {name}!', 'Greetings', { name })}</p>
    </section>

    <!-- t() — ICU plurals, the interactive playground's phrase. -->
    <section class="card">
        <h2><code>t()</code> — ICU plurals, from the interactive playground</h2>
        <p class="live">
            {$t('Hello, {name}! You have {count, plural, one {# new message} other {# new messages}}.', 'Greetings', {
                name,
                count: messages,
            })}
        </p>
        <div class="stepper" translate="no">
            <button aria-label="Fewer" onclick={() => (messages = Math.max(0, messages - 1))}>−</button>
            <span class="count">{messages}</span>
            <button aria-label="More" onclick={() => (messages += 1)}>+</button>
        </div>
        <p class="hint">Change count to 1 and back — the grammar follows. Every locale applies its own plural rules.</p>
    </section>

    <section class="card">
        <h2><code>&lt;Translate&gt;</code> — content block</h2>
        <div class="live">
            <Translate category="Home">
                <p>Welcome to our store. Browse the catalog in your language.</p>
            </Translate>
        </div>
    </section>

    <section class="card">
        <h2><code>&lt;Phrase&gt;</code> — params &amp; markup (<code>%name%</code>)</h2>
        <div class="live">
            <Phrase category="Cart" params={{ name: 'Sarah', count: items }}>
                Hi %name%, you have %count% items in your cart.
            </Phrase>
        </div>
        <div class="stepper" translate="no">
            <button aria-label="Fewer" onclick={() => (items = Math.max(0, items - 1))}>−</button>
            <span class="count">{items}</span>
            <button aria-label="More" onclick={() => (items += 1)}>+</button>
        </div>
    </section>

    <section class="card">
        <h2><code>&lt;DontTranslate&gt;</code> — never translated</h2>
        <div class="live">
            <Translate category="Tour">
                <p>Sign in with <DontTranslate>Langsys ID</DontTranslate> to continue.</p>
            </Translate>
        </div>
    </section>

    <footer class="meta" translate="no">
        loaded {$currentlyLoadedLocale || 'en-US'} ·
        <a href={DOCS_URL} target="_blank" rel="noopener noreferrer">How this works ↗</a>
    </footer>
</div>
