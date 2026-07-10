<script>
    import { t, currentlyLoadedLocale, Translate, Phrase, DontTranslate } from 'langsys-js-svelte';
    import { locale, LOCALES, LOCALE_LABELS } from './langsys';
    import Hood from './Hood.svelte';

    let xray = $state(false);
    let teams = $state(1200);

    const tCode = `import { t } from 'langsys-js-svelte';\n\n{$t('Ship faster in every market', 'Site')}`;
    const translateCode = `<Translate category="Site">\n  <p>Real-time machine translation…</p>\n</Translate>`;
    const phraseCode = `<Phrase category="Site" params={{ count }}>\n  Join %count% teams already translating with Langsys.\n</Phrase>`;
    const dontCode = `Powered by <DontTranslate>Langsys</DontTranslate>`;
</script>

<div class="hoodapp" class:xray>
    <header class="topbar">
        <div class="brand"><span class="logo">◆</span> <DontTranslate>Langsys</DontTranslate></div>
        <nav class="locales">
            {#each LOCALES as code}
                <button class={$currentlyLoadedLocale === code ? 'pill active' : 'pill'} onclick={() => locale.set(code)}>
                    {LOCALE_LABELS[code] ?? code}
                </button>
            {/each}
        </nav>
        <button class={xray ? 'xray-toggle on' : 'xray-toggle'} onclick={() => (xray = !xray)}>
            {$t(xray ? 'Hide the translation layer' : 'Reveal the translation layer', 'Site')}
        </button>
    </header>

    <section class="hero">
        <h1 class="ls-live">{$t('Ship your app in every language', 'Site')}</h1>
        <div class="ls-live hero-sub">
            <Translate category="Site"><p>This page is translating itself in real time. Switch the language above and watch every word change, no rebuild and no keys file.</p></Translate>
        </div>
        <button class="cta ls-live">{$t('Start free', 'Site')}</button>
        <p class="hint">{$t('Look under the hood', 'Site')} ↓</p>
    </section>

    <section class="feature">
        <h2 class="ls-live">{$t('The phrase is the key', 'Site')}</h2>
        <Hood code={tCode}>
            <span class="ls-live big">{$t('Ship faster in every market', 'Site')}</span>
        </Hood>
        <p class="cap ls-live">{$t('No keys file, no extraction step. The sentence in your code is both the key and its default.', 'Site')}</p>
    </section>

    <section class="feature">
        <h2 class="ls-live">{$t('Translate whole blocks', 'Site')}</h2>
        <Hood code={translateCode}>
            <div class="ls-live">
                <Translate category="Site"><p>Real-time machine translation across every locale you enable, powered by leading AI providers.</p></Translate>
            </div>
        </Hood>
        <p class="cap ls-live">{$t('One tag localizes an entire block of markup as a single unit.', 'Site')}</p>
    </section>

    <section class="feature">
        <h2 class="ls-live">{$t('Dynamic values and plurals', 'Site')}</h2>
        <Hood code={phraseCode}>
            <div class="phrase-row">
                <div class="ls-live">
                    <Phrase category="Site" params={{ count: teams }}>Join %count% teams already translating with Langsys.</Phrase>
                </div>
                <div class="stepper">
                    <button onclick={() => (teams = Math.max(1, teams - 1))}>−</button>
                    <span>{teams}</span>
                    <button onclick={() => (teams = teams + 1)}>+</button>
                </div>
            </div>
        </Hood>
        <p class="cap ls-live">{$t('Interpolation and correct plurals in every language, at render time.', 'Site')}</p>
    </section>

    <section class="feature">
        <h2 class="ls-live">{$t('Keep the untouchables', 'Site')}</h2>
        <Hood code={dontCode}>
            <span class="big">
                <span class="ls-live">{$t('Powered by', 'Site')}</span>
                <DontTranslate><span class="ls-frozen">Langsys</span></DontTranslate>
            </span>
        </Hood>
        <p class="cap ls-live">{$t('Brand names, code, and IDs stay exactly as written.', 'Site')}</p>
    </section>

    <section class="reveal">
        <p class="cap ls-live">{$t('Everything highlighted is translated live by Langsys. Nothing else is touched.', 'Site')}</p>
        <button class={xray ? 'xray-toggle on' : 'xray-toggle'} onclick={() => (xray = !xray)}>
            {$t(xray ? 'Hide the translation layer' : 'Reveal the translation layer', 'Site')}
        </button>
    </section>

    <section class="ctaband">
        <h2 class="ls-live">{$t('Add your first language in one line', 'Site')}</h2>
        <pre class="install"><code>npm install langsys-js-svelte</code></pre>
        <button class="cta ls-live">{$t('Read the docs', 'Site')}</button>
    </section>

    <footer class="footer">
        <span>Powered by <DontTranslate>Langsys</DontTranslate></span>
    </footer>
</div>
