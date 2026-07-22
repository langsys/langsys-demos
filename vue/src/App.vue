<script setup>
// The Vue demo app: every example on docs.langsys.dev/learn/sdk/vue running
// live, wired by the exact code the docs page shows.
import { computed, ref } from 'vue';
import { DontTranslate, Phrase, Translate, useCurrentLocale, useSignal, useT } from 'langsys-js-vue';
import Greeting from './Greeting.vue';
import { LOCALES, LOCALE_LABELS, demoBanner, locale } from './langsys';

const KEYS_URL = 'https://docs.langsys.dev/learn/concepts/keys-and-environments';
const DOCS_URL = 'https://docs.langsys.dev/learn/sdk/vue';

const t = useT();
const name = 'Sarah';

/* t() — ICU plurals, the interactive playground's phrase. Computed here
   because the ICU braces (`}}`) would end a template interpolation early. */
const messages = ref(3);
const inboxText = computed(() =>
    t('Hello, {name}! You have {count, plural, one {# new message} other {# new messages}}.', 'Greetings', {
        name,
        count: messages.value,
    }),
);

/* Phrase — params & markup. */
const items = ref(3);

/* Reading signals — Vue tracks only its own refs, so useSignal bridges the
   base-SDK signal; useCurrentLocale is the loaded-locale shortcut. */
const selected = useSignal(locale);
const loaded = useCurrentLocale();
const loadedOrDefault = computed(() => loaded.value || 'en-US');
</script>

<template>
    <div v-if="demoBanner" class="demo-banner" translate="no">
        <template v-if="demoBanner === 'shared'">
            <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones won't.
            Drop your own keys in <code>.env</code> to watch discovery register and translate your phrases live.
        </template>
        <template v-else>
            <strong>No Langsys credentials configured</strong> — showing source text only, nothing translates. Add
            your project id and key in <code>.env</code> to see it live.
        </template>
        <a :href="KEYS_URL" target="_blank" rel="noopener noreferrer">Get your keys →</a>
    </div>

    <div class="app">
        <header class="topbar">
            <div class="brand"><span class="logo">◆</span> <span translate="no">Langsys</span> × Vue</div>
            <nav class="locales" translate="no">
                <button
                    v-for="code in LOCALES"
                    :key="code"
                    class="pill"
                    :class="{ active: loadedOrDefault === code }"
                    @click="locale.set(code)"
                >
                    {{ LOCALE_LABELS[code] ?? code }}
                </button>
            </nav>
        </header>

        <section class="card">
            <h2><code>t()</code> — inline string, in a component</h2>
            <div class="live"><Greeting /></div>
        </section>

        <section class="card">
            <h2><code>t()</code> — ICU plurals, from the interactive playground</h2>
            <p class="live">{{ inboxText }}</p>
            <div class="stepper" translate="no">
                <button aria-label="Fewer" @click="messages = Math.max(0, messages - 1)">−</button>
                <span class="count">{{ messages }}</span>
                <button aria-label="More" @click="messages++">+</button>
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
                <Phrase category="Cart" :params="{ name: 'Sarah', count: items }">
                    Hi %name%, you have %count% items in your cart.
                </Phrase>
            </div>
            <div class="stepper" translate="no">
                <button aria-label="Fewer" @click="items = Math.max(0, items - 1)">−</button>
                <span class="count">{{ items }}</span>
                <button aria-label="More" @click="items++">+</button>
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
            selected {{ selected }} · loaded {{ loadedOrDefault }} ·
            <a :href="DOCS_URL" target="_blank" rel="noopener noreferrer">How this works ↗</a>
        </footer>
    </div>
</template>
