<script>
    import { t, currentlyLoadedLocale, Translate, Phrase, DontTranslate } from 'langsys-js-svelte';
    import { locale, LOCALES } from './langsys';
</script>

<main>
    <nav>
        {#each LOCALES as code}
            <button onclick={() => locale.set(code)} disabled={$currentlyLoadedLocale === code}>{code}</button>
        {/each}
    </nav>

    <!-- t() — the phrase is the key AND the base-language default -->
    <h1>{$t('Welcome to the Langsys store', 'Home')}</h1>

    <!-- <Translate> — a whole content block, translated as one unit -->
    <Translate category="Home"><p>Everything on this page translates in real time as you switch locale.</p></Translate>

    <!-- <Phrase> — params & markup (author placeholders as %name%, since Svelte
         consumes single-brace {name} as an expression) -->
    <Phrase category="Home" params={{ name: 'Sarah', count: 3 }}>Hi %name%, you have %count% items in your cart.</Phrase>

    <!-- <DontTranslate> — never translated -->
    <p>Powered by <DontTranslate>Langsys</DontTranslate>.</p>
</main>

<style>
    main {
        max-width: 640px;
        margin: 2rem auto;
        padding: 0 1rem;
        font-family: system-ui, sans-serif;
    }
    nav {
        display: flex;
        gap: 8px;
        margin-bottom: 24px;
    }
</style>
