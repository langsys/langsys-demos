<script setup lang="ts">
// Step 3 of docs.langsys.dev/learn/guides/nuxt: from here it's the plain Vue SDK — the same cards
// as the Vue demo, under the catalog the server seeded.
import type { Signal } from 'langsys-js-vue';
import { DontTranslate, Phrase, Translate, useCurrentLocale, useSignal, useT } from 'langsys-js-vue';
import type { Language } from '../langsys';

const KEYS_URL = 'https://docs.langsys.dev/learn/concepts/keys-and-environments';
const DOCS_URL = 'https://docs.langsys.dev/learn/guides/nuxt';

const sharedDemo = useRuntimeConfig().public.langsysSharedDemo;
const locale = inject<Signal<string>>('locale')!;
// The languages the project serves — the server read them, so the list is right from the first paint.
const languages = inject<Language[]>('languages')!;
const selected = useSignal(locale);
const loaded = useCurrentLocale();

const t = useT();
const name = 'Sarah';

/* Plurals, written flat: Langsys generates the plural forms per locale. Nobody types ICU. */
const MSG = 'Hello, {name}! You have {count} new messages.';
const messages = ref(3);
const items = ref(3);
</script>

<template>
    <div v-if="sharedDemo" class="demo-banner" translate="no">
        <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones won't.
        Drop your own keys in <code>.env</code> to watch discovery register and translate your phrases live.
        <a :href="KEYS_URL" target="_blank" rel="noopener noreferrer">Get your keys →</a>
    </div>

    <div class="app">
        <header class="topbar">
            <div class="brand"><span class="logo">◆</span> <span translate="no">Langsys</span> × Nuxt</div>
            <select
                class="locale-select"
                aria-label="Language"
                translate="no"
                :value="selected"
                @change="locale.set(($event.target as HTMLSelectElement).value)"
            >
                <option v-for="l in languages" :key="l.code" :value="l.code">{{ l.label }}</option>
            </select>
        </header>

        <section class="card">
            <h2><code>t()</code> — inline string, in a component</h2>
            <p class="live">{{ t('Hello, {name}!', 'Greetings', { name }) }}</p>
        </section>

        <section class="card">
            <h2><code>t()</code> — plurals, written flat</h2>
            <p class="live">{{ t(MSG, 'Greetings', { name, count: messages }) }}</p>
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
                    <h3>Welcome to our store</h3>
                    <p>Browse the catalog in your language.</p>
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
                    <p>Welcome! <DontTranslate>This sentence always stays in English.</DontTranslate> Thanks for visiting!</p>
                </Translate>
            </div>
        </section>

        <footer class="meta" translate="no">
            selected {{ selected }} · loaded {{ loaded || 'en-US' }} · seeded by the server ·
            <a :href="DOCS_URL" target="_blank" rel="noopener noreferrer">How this works ↗</a>
        </footer>
    </div>
</template>
