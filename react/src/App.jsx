import { useState } from 'react';
import { DontTranslate, Phrase, Translate, useCurrentLocale, useSignal, useT } from 'langsys-js-react';
import { demoBanner, languages, locale } from './langsys';
import './demo.css';

const KEYS_URL = 'https://docs.langsys.dev/learn/concepts/keys-and-environments';
const DOCS_URL = 'https://docs.langsys.dev/learn/sdk/react';

// The call behind each output, shown above it — the same code the app runs.
const CODE = {
    greeting: `t('Hello, {name}!', 'Greetings', { name })`,
    plural: `t(\n  'Hello, {name}! You have {count} new messages.',\n  'Greetings',\n  { name, count },\n)`,
    block: `<Translate category="Home">\n  <h3>Welcome to our store</h3>\n  <p>Browse the catalog in your language.</p>\n</Translate>`,
    phrase: `<Phrase category="Cart" params={{ name, count }}>\n  Hi %name%, you have %count% items in your cart.\n</Phrase>`,
    dont: `<Translate category="Tour">\n  <p>\n    Welcome!\n    <DontTranslate>\n      This sentence always stays in English.\n    </DontTranslate>\n    Thanks for visiting!\n  </p>\n</Translate>`,
    order: `t('Your order {id} ships on {date}.', 'Checkout', {\n  id: '48213',\n  date: new Date(2026, 7, 15),\n})`,
};
// Local midnight, so no timezone moves the day.
const SHIP_DATE = new Date(2026, 7, 15);

// The React demo app: every example on docs.langsys.dev/learn/sdk/react
// running live, wired by the exact code the docs page shows.

/* t() — inline string, in a component. */
function Greeting({ name }) {
    const t = useT();
    return <p>{t('Hello, {name}!', 'Greetings', { name })}</p>;
}

/* t() — plurals. The phrase is written flat; Langsys generates the plural
   forms per locale (the base locale included) and the SDK picks the branch
   from `count`. Nobody types ICU. */
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

/* The languages the project serves, read once the SDK has started. */
function LocaleSelect() {
    const selected = useSignal(locale);
    const offered = useSignal(languages);
    return (
        <select
            className="locale-select"
            aria-label="Language"
            translate="no"
            value={selected}
            onChange={(e) => locale.set(e.target.value)}
        >
            {offered.map((l) => (
                <option key={l.code} value={l.code}>
                    {l.label}
                </option>
            ))}
        </select>
    );
}

/* t() — values in a sentence are formatted per locale: the date here, numbers too. */
function Order() {
    const t = useT();
    return <p>{t('Your order {id} ships on {date}.', 'Checkout', { id: '48213', date: SHIP_DATE })}</p>;
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
                            <strong>Shared demo project (read-only)</strong> — existing phrases translate, but a read-only key can't add new ones. To watch a phrase you write get translated, <a href="https://github.com/langsys/langsys-demos/tree/main/react#use-your-own-project" target="_blank" rel="noopener noreferrer">run this app on your own project</a> or <a href="https://docs.langsys.dev/learn/quickstart" target="_blank" rel="noopener noreferrer">see it in the quickstart video</a>.
                        </>
                    ) : (
                        <>
                            <strong>No Langsys credentials configured</strong> — showing source text only, nothing
                            translates. Add your project id and key in <code>.env</code> to see it live.
                        </>
                    )}{' '}
                    <a href={KEYS_URL} target="_blank" rel="noopener noreferrer">
                        Get your keys
                    </a>
                </div>
            )}
            <div className="app">
                <header className="topbar">
                    <div className="brand">
                        <span className="logo">◆</span> <span translate="no">Langsys</span> × React
                    </div>
                    <LocaleSelect />
                </header>

                <section className="card">
                    <h2>
                        <code>t()</code> — inline string, in a component
                    </h2>
                    <pre className="call">
                        <code>{CODE.greeting}</code>
                    </pre>
                    <div className="live">
                        <Greeting name="Sarah" />
                    </div>
                </section>

                <section className="card">
                    <h2>
                        <code>t()</code> — plurals, written flat
                    </h2>
                    <pre className="call">
                        <code>{CODE.plural}</code>
                    </pre>
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
                    <pre className="call">
                        <code>{CODE.block}</code>
                    </pre>
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
                    <pre className="call">
                        <code>{CODE.phrase}</code>
                    </pre>
                    <div className="live">
                        <CartNote />
                    </div>
                </section>

                <section className="card">
                    <h2>
                        <code>t()</code> — dates and numbers, per locale
                    </h2>
                    <pre className="call">
                        <code>{CODE.order}</code>
                    </pre>
                    <div className="live">
                        <Order />
                    </div>
                    <p className="hint">The date is formatted for each locale; the order id is a string, so it stays as written.</p>
                </section>

                <section className="card">
                    <h2>
                        <code>&lt;DontTranslate&gt;</code> — never translated
                    </h2>
                    <pre className="call">
                        <code>{CODE.dont}</code>
                    </pre>
                    <div className="live">
                        <Translate category="Tour">
                            <p>
                                Welcome! <DontTranslate>This sentence always stays in English.</DontTranslate> Thanks for visiting!
                            </p>
                        </Translate>
                    </div>
                </section>

                <LocaleBadge />
            </div>
        </>
    );
}
