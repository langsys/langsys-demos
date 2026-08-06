import { Component, computed, inject, signal, type WritableSignal } from '@angular/core';
import { LANGSYS_IMPORTS, LangsysService } from 'langsys-js-angular';
import { GreetingComponent } from './greeting.component';
import { LOCALES, LOCALE_LABELS, demoBanner, locale } from './langsys';

// The Angular demo app: every example on docs.langsys.dev/learn/sdk/angular
// running live, wired by the exact code the docs page shows.
@Component({
    selector: 'app-root',
    standalone: true,
    imports: [LANGSYS_IMPORTS, GreetingComponent],
    template: `
        @if (demoBanner) {
            <div class="demo-banner" translate="no">
                @if (demoBanner === 'shared') {
                    <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones
                    won't. Drop your own keys in <code>.env</code> to watch discovery register and translate your
                    phrases live.
                } @else {
                    <strong>No Langsys credentials configured</strong> — showing source text only, nothing translates.
                    Add your project id and key in <code>.env</code> to see it live.
                }
                <a [href]="KEYS_URL" target="_blank" rel="noopener noreferrer">Get your keys →</a>
            </div>
        }

        <div class="app">
            <header class="topbar">
                <div class="brand"><span class="logo">◆</span> <span translate="no">Langsys</span> × Angular</div>
                <nav class="locales" translate="no">
                    @for (code of LOCALES; track code) {
                        <button class="pill" [class.active]="loadedOrDefault() === code" (click)="locale.set(code)">
                            {{ LOCALE_LABELS[code] || code }}
                        </button>
                    }
                </nav>
            </header>

            <section class="card">
                <h2><code>t()</code> — inline string, in a component</h2>
                <div class="live"><app-greeting /></div>
            </section>

            <section class="card">
                <h2><code>t()</code> — ICU plurals, from the interactive playground</h2>
                <p class="live">{{ MSG | t: 'Greetings' : { name: name, count: messages() } }}</p>
                <div class="stepper" translate="no">
                    <button aria-label="Fewer" (click)="dec(messages)">−</button>
                    <span class="count">{{ messages() }}</span>
                    <button aria-label="More" (click)="inc(messages)">+</button>
                </div>
                <p class="hint">
                    Change count to 1 and back — the grammar follows. Every locale applies its own plural rules.
                </p>
            </section>

            <section class="card">
                <h2><code>&lt;Translate&gt;</code> — content block</h2>
                <div class="live">
                    <div lsTranslate category="Home">
                        <h3>Welcome to our store</h3>
                        <p>Browse the catalog in your language.</p>
                    </div>
                </div>
            </section>

            <section class="card">
                <h2><code>&lt;Phrase&gt;</code> — params &amp; markup (<code>%name%</code>)</h2>
                <div class="live">
                    <span lsPhrase category="Cart" [params]="{ name: 'Sarah', count: items() }">
                        Hi %name%, you have %count% items in your cart.
                    </span>
                </div>
                <div class="stepper" translate="no">
                    <button aria-label="Fewer" (click)="dec(items)">−</button>
                    <span class="count">{{ items() }}</span>
                    <button aria-label="More" (click)="inc(items)">+</button>
                </div>
            </section>

            <section class="card">
                <h2><code>&lt;DontTranslate&gt;</code> — never translated</h2>
                <div class="live">
                    <div lsTranslate category="Tour">
                        <p>
                            Welcome! <span lsDontTranslate>This sentence always stays in English.</span> Thanks for
                            visiting!
                        </p>
                    </div>
                </div>
            </section>

            <footer class="meta" translate="no">
                selected {{ locale.locale() }} · loaded {{ loadedOrDefault() }} ·
                <a [href]="DOCS_URL" target="_blank" rel="noopener noreferrer">How this works ↗</a>
            </footer>
        </div>
    `,
})
export class AppComponent {
    private readonly langsys = inject(LangsysService);

    readonly KEYS_URL = 'https://docs.langsys.dev/learn/concepts/keys-and-environments';
    readonly DOCS_URL = 'https://docs.langsys.dev/learn/sdk/angular';

    readonly LOCALES = LOCALES;
    readonly LOCALE_LABELS = LOCALE_LABELS;
    readonly demoBanner = demoBanner;
    readonly locale = locale;
    readonly name = 'Sarah';

    // t() — ICU plurals, the interactive playground's phrase. Held as a field so
    // the ICU braces live in a string value, not literal template text (Angular
    // would parse literal `{…}` in the template as an ICU message).
    readonly MSG = 'Hello, {name}! You have {count, plural, one {# new message} other {# new messages}}.';
    readonly messages = signal(3);

    // <Phrase> — params & markup.
    readonly items = signal(3);

    // Loaded locale (lags the selection until the fetch settles).
    readonly loadedOrDefault = computed(() => this.langsys.currentLocale() || 'en-US');

    dec(s: WritableSignal<number>): void {
        s.set(Math.max(0, s() - 1));
    }
    inc(s: WritableSignal<number>): void {
        s.set(s() + 1);
    }
}
