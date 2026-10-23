// Step 3 of docs.langsys.dev/learn/guides/nextjs: from here it's the plain React SDK — the same
// cards as the React demo, under the catalog the server seeded.
'use client';

import { useState } from 'react';
import { DontTranslate, Phrase, Translate, useCurrentLocale, useT } from 'langsys-js-react';
import { useLocale } from './LangsysClient';

const KEYS_URL = 'https://docs.langsys.dev/learn/concepts/keys-and-environments';
const DOCS_URL = 'https://docs.langsys.dev/learn/guides/nextjs';

function Greeting({ name }) {
    const t = useT();
    return <p>{t('Hello, {name}!', 'Greetings', { name })}</p>;
}

/* Plurals, written flat: Langsys generates the plural forms per locale. Nobody types ICU. */
function Inbox({ name }) {
    const t = useT();
    const [count, setCount] = useState(3);
    return (
        <>
            <p>{t('Hello, {name}! You have {count} new messages.', 'Greetings', { name, count })}</p>
            <Stepper count={count} onChange={setCount} />
        </>
    );
}

/* %name%/%count% markers avoid JSX brace collisions. */
function CartNote() {
    const [count, setCount] = useState(3);
    return (
        <>
            <Phrase category="Cart" params={{ name: 'Sarah', count }}>
                Hi %name%, you have %count% items in your cart.
            </Phrase>
            <Stepper count={count} onChange={setCount} />
        </>
    );
}

/* The languages the project serves — the server read them, so the list is right from the first paint. */
function LocaleSelect() {
    const { selected, setLocale, languages } = useLocale();
    return (
        <select
            className="locale-select"
            aria-label="Language"
            translate="no"
            value={selected}
            onChange={(e) => setLocale(e.target.value)}
        >
            {languages.map((l) => (
                <option key={l.code} value={l.code}>
                    {l.label}
                </option>
            ))}
        </select>
    );
}

function Stepper({ count, onChange }) {
    return (
        <div className="stepper" translate="no">
            <button aria-label="Fewer" onClick={() => onChange(Math.max(0, count - 1))}>
                −
            </button>
            <span className="count">{count}</span>
            <button aria-label="More" onClick={() => onChange(count + 1)}>
                +
            </button>
        </div>
    );
}

function LocaleBadge() {
    const { selected } = useLocale();
    const loaded = useCurrentLocale();
    return (
        <footer className="meta" translate="no">
            selected {selected} · loaded {loaded || 'en-US'} · seeded by the server ·{' '}
            <a href={DOCS_URL} target="_blank" rel="noopener noreferrer">
                How this works ↗
            </a>
        </footer>
    );
}

export function Demo() {
    const { banner } = useLocale();
    return (
        <>
            {banner && (
                <div className="demo-banner" translate="no">
                    <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones
                    won't. Drop your own keys in <code>.env.local</code> to watch discovery register and translate your
                    phrases live.{' '}
                    <a href={KEYS_URL} target="_blank" rel="noopener noreferrer">
                        Get your keys →
                    </a>
                </div>
            )}
            <div className="app">
                <header className="topbar">
                    <div className="brand">
                        <span className="logo">◆</span> <span translate="no">Langsys</span> × Next.js
                    </div>
                    <LocaleSelect />
                </header>

                <section className="card">
                    <h2>
                        <code>t()</code> — inline string, in a Client Component
                    </h2>
                    <div className="live">
                        <Greeting name="Sarah" />
                    </div>
                </section>

                <section className="card">
                    <h2>
                        <code>t()</code> — plurals, written flat
                    </h2>
                    <div className="live">
                        <Inbox name="Sarah" />
                    </div>
                    <p className="hint">
                        Change count to 1 and back — the grammar follows. Every locale applies its own plural rules.
                    </p>
                </section>

                <section className="card">
                    <h2>
                        <code>&lt;Translate&gt;</code> — content block
                    </h2>
                    <div className="live">
                        <Translate category="Home">
                            <h3>Welcome to our store</h3>
                            <p>Browse the catalog in your language.</p>
                        </Translate>
                    </div>
                </section>

                <section className="card">
                    <h2>
                        <code>&lt;Phrase&gt;</code> — params &amp; markup
                    </h2>
                    <div className="live">
                        <CartNote />
                    </div>
                </section>

                <section className="card">
                    <h2>
                        <code>&lt;DontTranslate&gt;</code> — never translated
                    </h2>
                    <div className="live">
                        <Translate category="Tour">
                            <p>
                                Welcome! <DontTranslate>This sentence always stays in English.</DontTranslate> Thanks
                                for visiting!
                            </p>
                        </Translate>
                    </div>
                </section>

                <LocaleBadge />
            </div>
        </>
    );
}
