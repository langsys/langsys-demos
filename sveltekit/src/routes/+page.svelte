<script>
    // Step 3 of docs.langsys.dev/learn/guides/sveltekit: from here it's the plain Svelte SDK — the
    // same cards as the Svelte demo, under the catalog the server load seeded.
    import { getContext } from 'svelte';
    import { DontTranslate, Phrase, Translate, currentlyLoadedLocale, t } from 'langsys-js-svelte';
    import { LOCALES, LOCALE_LABELS } from '$lib/langsys';

    const KEYS_URL = 'https://docs.langsys.dev/learn/concepts/keys-and-environments';
    const DOCS_URL = 'https://docs.langsys.dev/learn/guides/sveltekit';

    let { data } = $props();
    const locale = getContext('locale');

    const name = 'Sarah';
    let messages = $state(3);
    let items = $state(3);
</script>

{#if data.banner}
    <div class="demo-banner" translate="no">
        <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones won't.
        Drop your own keys in <code>.env</code> to watch discovery register and translate your phrases live.
        <a href={KEYS_URL} target="_blank" rel="noopener noreferrer">Get your keys →</a>
    </div>
{/if}

<div class="app">
    <header class="topbar">
        <div class="brand"><span class="logo">◆</span> <span translate="no">Langsys</span> × SvelteKit</div>
        <nav class="locales" translate="no">
            {#each LOCALES as code}
                <button class={$locale === code ? 'pill active' : 'pill'} onclick={() => locale.set(code)}>
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

    <!-- t() — plurals, written flat: Langsys generates the plural forms per locale; nobody types ICU. -->
    <section class="card">
        <h2><code>t()</code> — plurals, written flat</h2>
        <p class="live">
            {$t('Hello, {name}! You have {count} new messages.', 'Greetings', {
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
                <h3>Welcome to our store</h3>
                <p>Browse the catalog in your language.</p>
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
                <p>Welcome! <DontTranslate>This sentence always stays in English.</DontTranslate> Thanks for visiting!</p>
            </Translate>
        </div>
    </section>

    <footer class="meta" translate="no">
        selected {$locale} · loaded {$currentlyLoadedLocale || 'en-US'} · seeded by the server ·
        <a href={DOCS_URL} target="_blank" rel="noopener noreferrer">How this works ↗</a>
    </footer>
</div>
