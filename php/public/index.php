<?php
// The PHP demo app: the examples on docs.langsys.dev/learn/sdk/php running live, with the plain
// langsys/langsys-php client and no framework. Translation happens on the server — view source:
// the HTML arrives already localized.

require __DIR__ . '/../vendor/autoload.php';
require __DIR__ . '/../helpers.php';

$active = demo_locale();
$count = max(0, min(99, (int) ($_GET['count'] ?? 3)));
$link = fn (array $query) => '?' . http_build_query($query + ['locale' => $active, 'count' => $count]);

// Which banner the page shows: null when you supplied your own credentials.
$banner = getenv('LANGSYS_PROJECT_ID') ? null : 'shared';

// translate() works anywhere in PHP, not only in templates — computed here, before any output.
$orderTitle = langsys()->translate('Order confirmed', null, 'Checkout');
$orderBody = langsys()->translate('Your order {id} ships on {date}.', null, 'Checkout', null, [
    'id' => '48213', // a string, so it skips number formatting
    'date' => new DateTimeImmutable('2026-08-15'), // locale-formatted
]);
?>
<!doctype html>
<html lang="<?= $active ?>">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Langsys × PHP — demo</title>
    <link rel="stylesheet" href="demo.css">
</head>
<body>
    <?php if ($banner): ?>
        <div class="demo-banner" translate="no">
            <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones
            won't. Set <code>LANGSYS_PROJECT_ID</code> and <code>LANGSYS_API_KEY</code> to watch discovery
            register and translate your phrases live.
            <a href="https://docs.langsys.dev/learn/concepts/keys-and-environments" target="_blank"
                rel="noopener noreferrer">Get your keys →</a>
        </div>
    <?php endif ?>

    <div class="app">
        <header class="topbar">
            <div class="brand">
                <span class="logo">◆</span> <span translate="no">Langsys</span> × PHP
            </div>
            <!-- Server-rendered locale switcher: plain links. The helper saves ?locale= in a cookie. -->
            <nav class="locales" translate="no">
                <?php foreach (LOCALES as $code => $label): ?>
                    <a class="pill<?= $active === $code ? ' active' : '' ?>" href="<?= $link(['locale' => $code]) ?>"><?= $label ?></a>
                <?php endforeach ?>
            </nav>
        </header>

        <section class="card">
            <h2><code>t()</code> — inline string, in a template</h2>
            <div class="live">
                <p><?= t('Hello, {name}!', 'Greetings', ['name' => 'Sarah']) ?></p>
            </div>
        </section>

        <section class="card">
            <h2><code>t()</code> — plurals, written flat</h2>
            <div class="live">
                <p><?= t('Hello, {name}! You have {count} new messages.', 'Greetings', ['name' => 'Sarah', 'count' => $count]) ?></p>
                <div class="stepper" translate="no">
                    <a aria-label="Fewer" href="<?= $link(['count' => max(0, $count - 1)]) ?>">−</a>
                    <span class="count"><?= $count ?></span>
                    <a aria-label="More" href="<?= $link(['count' => $count + 1]) ?>">+</a>
                </div>
            </div>
            <p class="hint">
                Change count to 1 and back — the grammar follows. Every locale applies its own plural rules,
                resolved on the server by ICU.
            </p>
        </section>

        <section class="card">
            <h2><code>translate()</code> — anywhere in PHP</h2>
            <div class="live">
                <p><?= htmlspecialchars($orderTitle) ?></p>
                <p><?= htmlspecialchars($orderBody) ?></p>
            </div>
            <p class="hint">
                Computed before the template with <code>translate()</code> — the same call works in controllers,
                workers and CLI scripts. The date is formatted for the locale; the order id is a string, so it stays
                unformatted.
            </p>
        </section>

        <section class="card">
            <h2>Categories — same phrase, different meaning</h2>
            <div class="live">
                <p>
                    <strong><?= t('Home', 'Main Menu') ?></strong> · <strong><?= t('Home', 'Home repairs') ?></strong>
                </p>
            </div>
            <p class="hint">
                The category scopes the phrase, so the same words translate differently per context — in Spanish,
                "Inicio" for the menu entry and "Casa" for the service.
            </p>
        </section>

        <section class="card">
            <h2>Explicit coverage — untagged text never translates</h2>
            <div class="live">
                <p><?= t('Welcome!', 'Tour') ?> This sentence always stays in English. <?= t('Thanks for visiting!', 'Tour') ?></p>
            </div>
            <p class="hint">
                Only strings passed through <code>t()</code> are translated. The middle sentence isn't, so it passes
                through verbatim — no opt-out marker needed.
            </p>
        </section>

        <footer class="meta" translate="no">
            locale: <?= $active ?> · server-rendered ·
            <a href="https://docs.langsys.dev/learn/sdk/php" target="_blank" rel="noopener noreferrer">
                How this works ↗
            </a>
        </footer>
    </div>
</body>
</html>
