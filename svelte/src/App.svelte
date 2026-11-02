<script>
    // The Svelte demo app: every example on docs.langsys.dev/learn/sdk/svelte
    // running live, wired by the exact code the docs page shows.
    import { DontTranslate, Phrase, Translate, currentlyLoadedLocale, t } from 'langsys-js-svelte';
    import { demoBanner, languages, locale } from './langsys';

    const KEYS_URL = 'https://docs.langsys.dev/learn/concepts/keys-and-environments';
    const DOCS_URL = 'https://docs.langsys.dev/learn/sdk/svelte';

    // The call behind each output, shown above it — the same code the app runs.
    const CODE = {
        greeting: `$t('Hello, {name}!', 'Greetings', { name })`,
        plural: `$t(\n  'Hello, {name}! You have {count} new messages.',\n  'Greetings',\n  { name, count },\n)`,
        block: `<Translate category="Home">\n  <h3>Welcome to our store</h3>\n  <p>Browse the catalog in your language.</p>\n</Translate>`,
        phrase: `<Phrase category="Cart" params={{ name, count }}>\n  Hi %name%, you have %count% items in your cart.\n</Phrase>`,
        dont: `<Translate category="Tour">\n  <p>\n    Welcome!\n    <DontTranslate>\n      This sentence always stays in English.\n    </DontTranslate>\n    Thanks for visiting!\n  </p>\n</Translate>`,
        order: `$t('Your order {id} ships on {date}.', 'Checkout', {\n  id: '48213',\n  date: new Date(2026, 7, 15),\n})`,
    };
    // Local midnight, so no timezone moves the day.
    const shipDate = new Date(2026, 7, 15);

    const name = 'Sarah';
    let messages = $state(3);
    let items = $state(3);
</script>

{#if demoBanner}
    <div class="demo-banner" translate="no">
        {#if demoBanner === 'shared'}
            <strong>Shared demo project (read-only)</strong> — existing phrases translate, but a read-only key can't add new ones. To watch a phrase you write get translated, <a href="https://github.com/langsys/langsys-demos/tree/main/svelte#use-your-own-project" target="_blank" rel="noopener noreferrer">run this app on your own project</a> or <a href="https://docs.langsys.dev/learn/quickstart" target="_blank" rel="noopener noreferrer">see it in the quickstart video</a>.
        {:else}
            <strong>No Langsys credentials configured</strong> — showing source text only, nothing translates. Add
            your project id and key in <code>.env</code> to see it live.
        {/if}
        <a href={KEYS_URL} target="_blank" rel="noopener noreferrer">Get your keys</a>
    </div>
{/if}

<div class="app">
    <header class="topbar">
        <div class="brand"><span class="logo">◆</span> <span translate="no">Langsys</span> × Svelte</div>
        <!-- The languages the project serves, read once the SDK has started. -->
        <select class="locale-select" aria-label="Language" translate="no" bind:value={$locale}>
            {#each $languages as l (l.code)}
                <option value={l.code}>{l.label}</option>
            {/each}
        </select>
    </header>

    <!-- t() — inline string: the $t store re-reads on locale/catalog change. -->
    <section class="card">
        <h2><code>t()</code> — inline string, in a component</h2>
        <pre class="call"><code>{CODE.greeting}</code></pre>
        <p class="live">{$t('Hello, {name}!', 'Greetings', { name })}</p>
    </section>

    <!-- t() — plurals, written flat: Langsys generates the plural forms per locale; nobody types ICU. -->
    <section class="card">
        <h2><code>t()</code> — plurals, written flat</h2>
        <pre class="call"><code>{CODE.plural}</code></pre>
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
        <pre class="call"><code>{CODE.block}</code></pre>
        <div class="live">
            <Translate category="Home">
                <h3>Welcome to our store</h3>
                <p>Browse the catalog in your language.</p>
            </Translate>
        </div>
    </section>

    <section class="card">
        <h2><code>&lt;Phrase&gt;</code> — params &amp; markup (<code>%name%</code>)</h2>
        <pre class="call"><code>{CODE.phrase}</code></pre>
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
        <h2><code>t()</code> — dates and numbers, per locale</h2>
        <pre class="call"><code>{CODE.order}</code></pre>
        <p class="live">{$t('Your order {id} ships on {date}.', 'Checkout', { id: '48213', date: shipDate })}</p>
        <p class="hint">The date is formatted for each locale; the order id is a string, so it stays as written.</p>
    </section>

    <section class="card">
        <h2><code>&lt;DontTranslate&gt;</code> — never translated</h2>
        <pre class="call"><code>{CODE.dont}</code></pre>
        <div class="live">
            <Translate category="Tour">
                <p>Welcome! <DontTranslate>This sentence always stays in English.</DontTranslate> Thanks for visiting!</p>
            </Translate>
        </div>
    </section>

    <footer class="meta" translate="no">
        loaded {$currentlyLoadedLocale || 'en-US'} ·
        <a href={DOCS_URL} target="_blank" rel="noopener noreferrer">How this works ↗</a>
    </footer>
</div>
