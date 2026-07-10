import { useState } from 'react';
import { DontTranslate, Phrase, Translate, useCurrentLocale, useT } from 'langsys-js-react';
import { LOCALES, LOCALE_LABELS, locale } from './langsys';
import './store.css';

// Product names stay in <DontTranslate> (brand names); everything else — headings,
// descriptions, buttons, the cart line — is discovered and translated by Langsys.
const PRODUCTS = [
    {
        id: 'aurora',
        name: 'Aurora Headphones',
        emoji: '🎧',
        price: 299,
        desc: 'Wireless over-ear headphones with 40-hour battery life.',
    },
    {
        id: 'nimbus',
        name: 'Nimbus Keyboard',
        emoji: '⌨️',
        price: 149,
        desc: 'A low-profile mechanical keyboard for all-day comfort.',
    },
    {
        id: 'solaris',
        name: 'Solaris Lamp',
        emoji: '💡',
        price: 89,
        desc: 'A warm desk lamp that adapts to the time of day.',
    },
];

export default function App() {
    const t = useT();
    const current = useCurrentLocale();
    const [cart, setCart] = useState(0);

    return (
        <div className="app">
            <header className="topbar">
                <div className="brand">
                    <span className="logo">◆</span> <DontTranslate>Langsys</DontTranslate> Store
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
                <div className="cart-badge" title="cart">🛒 {cart}</div>
            </header>

            <div className="banner">{t('Free shipping on orders over $100', 'Store')}</div>

            <section className="hero">
                <h1>{t('Welcome to the Langsys store', 'Store')}</h1>
                <Translate category="Store">
                    <p className="lede">
                        Every word on this page is translated live as you switch language — no keys file, no rebuild.
                    </p>
                </Translate>
            </section>

            <section className="products">
                <h2>{t('Featured products', 'Store')}</h2>
                <div className="grid">
                    {PRODUCTS.map((product) => (
                        <article className="card" key={product.id}>
                            <div className="thumb">{product.emoji}</div>
                            <h3>
                                <DontTranslate>{product.name}</DontTranslate>
                            </h3>
                            <p className="desc">{t(product.desc, 'Store')}</p>
                            <div className="card-row">
                                <span className="price">${product.price}</span>
                                <button className="btn" onClick={() => setCart((count) => count + 1)}>
                                    {t('Add to cart', 'Store')}
                                </button>
                            </div>
                        </article>
                    ))}
                </div>
            </section>

            <aside className="cart">
                <h2>{t('Your cart', 'Store')}</h2>
                <Phrase category="Store" params={{ name: 'Sarah', count: cart }}>
                    Hi %name%, you have %count% items in your cart.
                </Phrase>
                <button className="btn btn-primary">{t('Checkout', 'Store')}</button>
            </aside>

            <footer className="footer">
                <span>
                    Powered by <DontTranslate>Langsys</DontTranslate>
                </span>
                <span>{t('All prices in USD', 'Store')}</span>
            </footer>
        </div>
    );
}
