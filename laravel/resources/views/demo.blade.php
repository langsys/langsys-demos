{{-- The Laravel demo app: every example on docs.langsys.dev/learn/sdk/laravel
     running live, wired by the exact code the docs page shows. Translation
     happens on the server — view source: the HTML arrives already localized. --}}
<!doctype html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Langsys × Laravel — demo</title>
    <link rel="stylesheet" href="{{ asset('demo.css') }}">
</head>
<body>
    @if ($banner)
        <div class="demo-banner" translate="no">
            @if ($banner === 'shared')
                <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones
                won't. Drop your own keys in <code>.env</code> to watch discovery register and translate your
                phrases live.
            @else
                <strong>No Langsys credentials configured</strong> — showing source text only, nothing translates.
                Add your project id and key in <code>.env</code> to see it live.
            @endif
            <a href="https://docs.langsys.dev/learn/concepts/keys-and-environments" target="_blank"
                rel="noopener noreferrer">Get your keys →</a>
        </div>
    @endif

    <div class="app">
        <header class="topbar">
            <div class="brand">
                <span class="logo">◆</span> <span translate="no">Langsys</span> × Laravel
            </div>
            {{-- Server-rendered locale switcher: plain links. DetectLocale picks
                 up ?locale= and persists it (cookie), so navigation keeps it. --}}
            <nav class="locales" translate="no">
                @foreach ($locales as $code => $label)
                    <a class="pill{{ $active === $code ? ' active' : '' }}"
                        href="?{{ http_build_query(['locale' => $code, 'count' => $count]) }}">{{ $label }}</a>
                @endforeach
            </nav>
        </header>

        <section class="card">
            <h2><code>@@t</code> — inline string, in Blade</h2>
            <div class="live">
                <p>@t('Hello, {name}!', 'Greetings', ['name' => 'Sarah'])</p>
            </div>
        </section>

        <section class="card">
            <h2><code>@@t</code> — ICU plurals, from the interactive playground</h2>
            <div class="live">
                <p>@t('Hello, {name}! You have {count, plural, one {# new message} other {# new messages}}.', 'Greetings', ['name' => 'Sarah', 'count' => $count])</p>
                <div class="stepper" translate="no">
                    <a aria-label="Fewer" href="?{{ http_build_query(['locale' => $active, 'count' => max(0, $count - 1)]) }}">−</a>
                    <span class="count">{{ $count }}</span>
                    <a aria-label="More" href="?{{ http_build_query(['locale' => $active, 'count' => $count + 1]) }}">+</a>
                </div>
            </div>
            <p class="hint">
                Change count to 1 and back — the grammar follows. Every locale applies its own plural rules,
                resolved server-side by ICU.
            </p>
        </section>

        <section class="card">
            <h2><code>t()</code> — anywhere in PHP</h2>
            <div class="live">
                <p>{{ $orderTitle }}</p>
                <p>{{ $orderBody }}</p>
            </div>
            <p class="hint">
                Computed in the route with <code>t()</code> — the same helper works in controllers, Livewire, jobs,
                and mail. The date is locale-formatted by the interpolator; the order id is a string, so it stays
                unformatted.
            </p>
        </section>

        <section class="card">
            <h2>Categories — same phrase, different meaning</h2>
            <div class="live">
                <p>
                    <strong>@t('Home', 'Main Menu')</strong> · <strong>@t('Home', 'Home repairs')</strong>
                </p>
            </div>
            <p class="hint">
                The category scopes the phrase, so the same words translate differently per context — in Spanish,
                "Inicio" for the menu entry and "Hogar" for the service.
            </p>
        </section>

        <section class="card">
            <h2>Explicit coverage — untagged text never translates</h2>
            <div class="live">
                <p>@t('Welcome!', 'Tour') This sentence always stays in English. @t('Thanks for visiting!', 'Tour')</p>
            </div>
            <p class="hint">
                Coverage is explicit: only strings wrapped in <code>@@t</code> / <code>t()</code> are translated.
                The middle sentence is untagged, so it passes through verbatim — no opt-out marker needed.
            </p>
        </section>

        <footer class="meta" translate="no">
            locale: {{ $active }} · server-rendered ·
            <a href="https://docs.langsys.dev/learn/sdk/laravel" target="_blank" rel="noopener noreferrer">
                How this works ↗
            </a>
        </footer>
    </div>
</body>
</html>
