import { DontTranslate, Phrase, Translate, useCurrentLocale, useT } from 'langsys-js-react';
import { LOCALES, locale } from './langsys';

export default function App() {
    const t = useT();
    const current = useCurrentLocale();

    return (
        <main style={{ maxWidth: 640, margin: '2rem auto', padding: '0 1rem', fontFamily: 'system-ui, sans-serif' }}>
            <nav style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
                {LOCALES.map((code) => (
                    <button key={code} onClick={() => locale.set(code)} disabled={current === code}>
                        {code}
                    </button>
                ))}
            </nav>

            {/* t() — the phrase is the key AND the base-language default */}
            <h1>{t('Welcome to the Langsys store', 'Home')}</h1>

            {/* <Translate> — a whole content block, translated as one unit */}
            <Translate category="Home">
                <p>Everything on this page translates in real time as you switch locale.</p>
            </Translate>

            {/* <Phrase> — params & markup (author placeholders as %name%) */}
            <Phrase category="Home" params={{ name: 'Sarah', count: 3 }}>
                Hi %name%, you have %count% items in your cart.
            </Phrase>

            {/* <DontTranslate> — never translated */}
            <p>
                Powered by <DontTranslate>Langsys</DontTranslate>.
            </p>
        </main>
    );
}
