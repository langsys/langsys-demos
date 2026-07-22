import { useState } from 'react';
import { DontTranslate, Phrase, Translate, useCurrentLocale, useSignal, useT } from 'langsys-js-react';
import { LOCALES, LOCALE_LABELS, demoBanner, locale } from './langsys';
import './demo.css';

const KEYS_URL = 'https://docs.langsys.dev/learn/concepts/keys-and-environments';
const DOCS_URL = 'https://docs.langsys.dev/learn/sdk/react';

// The React demo app: every example on docs.langsys.dev/learn/sdk/react
// running live, wired by the exact code the docs page shows.

/* t() — inline string, in a component. */
function Greeting({ name }) {
    const t = useT();
    return <p>{t('Hello, {name}!', 'Greetings', { name })}</p>;
}

/* t() — ICU plurals, the interactive playground's phrase. */
function Inbox({ name }) {
    const t = useT();
    const [count, setCount] = useState(3);
    return (
        <>
            <p>
                {t(
                    'Hello, {name}! You have {count, plural, one {# new message} other {# new messages}}.',
                    'Greetings',
                    { name, count },
                )}
            </p>
            <Stepper count={count} onChange={setCount} />
        </>
    );
}

/* Phrase — params & markup; %name%/%count% markers avoid JSX brace collisions. */
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

/* Reading signals — React re-renders only on React state, so useSignal
   bridges the base-SDK signal; useCurrentLocale is the loaded-locale shortcut. */
function LocaleBadge() {
    const selected = useSignal(locale);
    const loaded = useCurrentLocale();

    return (
        <footer className="meta" translate="no">
            selected {selected} · loaded {loaded || 'en-US'} ·{' '}
            <a href={DOCS_URL} target="_blank" rel="noopener noreferrer">
                How this works ↗
            </a>
        </footer>
    );
}

function LocalePills() {
    const loaded = useCurrentLocale();
    return (
        <nav className="locales" translate="no">
            {LOCALES.map((code) => (
                <button
                    key={code}
                    className={'pill' + ((loaded || 'en-US') === code ? ' active' : '')}
                    onClick={() => locale.set(code)}
                >
                    {LOCALE_LABELS[code] ?? code}
                </button>
            ))}
        </nav>
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

export default function App() {
    return (
        <>
            {demoBanner && (
                <div className="demo-banner" translate="no">
                    {demoBanner === 'shared' ? (
                        <>
                            <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or
                            edited ones won't. Drop your own keys in <code>.env</code> to watch discovery register and
                            translate your phrases live.
                        </>
                    ) : (
                        <>
                            <strong>No Langsys credentials configured</strong> — showing source text only, nothing
                            translates. Add your project id and key in <code>.env</code> to see it live.
                        </>
                    )}{' '}
                    <a href={KEYS_URL} target="_blank" rel="noopener noreferrer">
                        Get your keys →
                    </a>
                </div>
            )}
            <div className="app">
                <header className="topbar">
                    <div className="brand">
                        <span className="logo">◆</span> <span translate="no">Langsys</span> × React
                    </div>
                    <LocalePills />
                </header>

                <section className="card">
                    <h2>
                        <code>t()</code> — inline string, in a component
                    </h2>
                    <div className="live">
                        <Greeting name="Sarah" />
                    </div>
                </section>

                <section className="card">
                    <h2>
                        <code>t()</code> — ICU plurals, from the interactive playground
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
                            <p>Welcome to our store. Browse the catalog in your language.</p>
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
                                Sign in with <DontTranslate>Langsys ID</DontTranslate> to continue.
                            </p>
                        </Translate>
                    </div>
                </section>

                <LocaleBadge />
            </div>
        </>
    );
}
