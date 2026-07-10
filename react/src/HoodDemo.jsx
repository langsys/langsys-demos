import { useState } from 'react';
import { DontTranslate, Phrase, Translate, useCurrentLocale, useT } from 'langsys-js-react';
import { LOCALES, LOCALE_LABELS, locale } from './langsys';
import './hood.css';

// A "look under the hood" page: each Langsys feature is shown as the SDK code
// paired with its live rendered output — and the whole page promotes Langsys
// while translating itself in real time.

function Hood({ code, children }) {
    return (
        <div className="hood">
            <div className="hood-code">
                <div className="chrome">
                    <span className="dot" /> <span className="dot" /> <span className="dot" />
                    <span className="chrome-name">App.jsx</span>
                </div>
                <pre>
                    <code>{code}</code>
                </pre>
            </div>
            <div className="hood-arrow">renders ↓</div>
            <div className="hood-render">
                <div className="chrome browser">
                    <span className="dot" /> <span className="dot" /> <span className="dot" />
                    <span className="chrome-name">live</span>
                </div>
                <div className="hood-output">{children}</div>
            </div>
        </div>
    );
}

export default function HoodDemo() {
    const t = useT();
    const current = useCurrentLocale();
    const [xray, setXray] = useState(false);
    const [teams, setTeams] = useState(1200);

    return (
        <div className={xray ? 'hoodapp xray' : 'hoodapp'}>
            <header className="topbar">
                <div className="brand">
                    <span className="logo">◆</span> <DontTranslate>Langsys</DontTranslate>
                </div>
                <nav className="locales">
                    {LOCALES.map((code) => (
                        <button
                            key={code}
                            className={current === code ? 'pill active' : 'pill'}
                            onClick={() => locale.set(code)}
                        >
                            {LOCALE_LABELS[code] ?? code}
                        </button>
                    ))}
                </nav>
                <button className={xray ? 'xray-toggle on' : 'xray-toggle'} onClick={() => setXray((v) => !v)}>
                    {t(xray ? 'Hide the translation layer' : 'Reveal the translation layer', 'Site')}
                </button>
            </header>

            <section className="hero">
                <h1 className="ls-live">{t('Ship your app in every language', 'Site')}</h1>
                <div className="ls-live hero-sub">
                    <Translate category="Site">
                        <p>This page is translating itself in real time. Switch the language above and watch every word change, no rebuild and no keys file.</p>
                    </Translate>
                </div>
                <button className="cta ls-live">{t('Start free', 'Site')}</button>
                <p className="hint">{t('Look under the hood', 'Site')} ↓</p>
            </section>

            <section className="feature">
                <h2 className="ls-live">{t('The phrase is the key', 'Site')}</h2>
                <Hood code={`const t = useT();\n\nt('Ship faster in every market', 'Site')`}>
                    <span className="ls-live big">{t('Ship faster in every market', 'Site')}</span>
                </Hood>
                <p className="cap ls-live">
                    {t('No keys file, no extraction step. The sentence in your code is both the key and its default.', 'Site')}
                </p>
            </section>

            <section className="feature">
                <h2 className="ls-live">{t('Translate whole blocks', 'Site')}</h2>
                <Hood code={`<Translate category="Site">\n  <p>Real-time machine translation…</p>\n</Translate>`}>
                    <div className="ls-live">
                        <Translate category="Site">
                            <p>Real-time machine translation across every locale you enable, powered by leading AI providers.</p>
                        </Translate>
                    </div>
                </Hood>
                <p className="cap ls-live">{t('One tag localizes an entire block of markup as a single unit.', 'Site')}</p>
            </section>

            <section className="feature">
                <h2 className="ls-live">{t('Dynamic values and plurals', 'Site')}</h2>
                <Hood code={`<Phrase category="Site" params={{ count }}>\n  Join %count% teams already translating with Langsys.\n</Phrase>`}>
                    <div className="phrase-row">
                        <div className="ls-live">
                            <Phrase category="Site" params={{ count: teams }}>
                                Join %count% teams already translating with Langsys.
                            </Phrase>
                        </div>
                        <div className="stepper">
                            <button onClick={() => setTeams((n) => Math.max(1, n - 1))}>−</button>
                            <span>{teams}</span>
                            <button onClick={() => setTeams((n) => n + 1)}>+</button>
                        </div>
                    </div>
                </Hood>
                <p className="cap ls-live">{t('Interpolation and correct plurals in every language, at render time.', 'Site')}</p>
            </section>

            <section className="feature">
                <h2 className="ls-live">{t('Keep the untouchables', 'Site')}</h2>
                <Hood code={`Powered by <DontTranslate>Langsys</DontTranslate>`}>
                    <span className="big">
                        <span className="ls-live">{t('Powered by', 'Site')}</span>{' '}
                        <DontTranslate>
                            <span className="ls-frozen">Langsys</span>
                        </DontTranslate>
                    </span>
                </Hood>
                <p className="cap ls-live">{t('Brand names, code, and IDs stay exactly as written.', 'Site')}</p>
            </section>

            <section className="reveal">
                <p className="cap ls-live">
                    {t('Everything highlighted is translated live by Langsys. Nothing else is touched.', 'Site')}
                </p>
                <button className={xray ? 'xray-toggle on' : 'xray-toggle'} onClick={() => setXray((v) => !v)}>
                    {t(xray ? 'Hide the translation layer' : 'Reveal the translation layer', 'Site')}
                </button>
            </section>

            <section className="ctaband">
                <h2 className="ls-live">{t('Add your first language in one line', 'Site')}</h2>
                <pre className="install">
                    <code>npm install langsys-js-react</code>
                </pre>
                <button className="cta ls-live">{t('Read the docs', 'Site')}</button>
            </section>

            <footer className="footer">
                <span>
                    Powered by <DontTranslate>Langsys</DontTranslate>
                </span>
            </footer>
        </div>
    );
}
