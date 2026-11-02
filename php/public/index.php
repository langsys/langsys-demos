<?php
// The PHP demo app: the examples on docs.langsys.dev/learn/sdk/php running live, with the plain
// langsys/langsys-php client and no framework. Translation happens on the server — view source:
// the HTML arrives already localized.

require __DIR__ . '/../vendor/autoload.php';
require __DIR__ . '/../helpers.php';

// The call behind each output, shown above it — the same code the page runs.
const CODE = [
    'greeting' => "<?= t('Hello, {name}!', 'Greetings', ['name' => 'Sarah']) ?>",
    'plural' => "<?= t('Hello, {name}! You have {count} new messages.', 'Greetings', [\n    'name' => 'Sarah',\n    'count' => \$count,\n]) ?>",
    'order' => "translate('Your order {id} ships on {date}.', 'Checkout', [\n    'id' => '48213',\n    'date' => new DateTimeImmutable('2026-08-15'),\n])",
    'categories' => "<?= t('Home', 'Main Menu') ?>\n<?= t('Home', 'Home repairs') ?>",
    'coverage' => "<?= t('Welcome!', 'Tour') ?>\nThis sentence always stays in English.\n<?= t('Thanks for visiting!', 'Tour') ?>",
];

$active = demo_locale();
$count = max(0, min(99, (int) ($_GET['count'] ?? 3)));
$link = fn (array $query) => '?' . http_build_query($query + ['locale' => $active, 'count' => $count]);

// Which banner the page shows: null when you supplied your own credentials.
$banner = getenv('LANGSYS_PROJECT_ID') ? null : 'shared';

// translate() works anywhere in PHP, not only in templates — computed here, before any output.
$orderTitle = translate('Order confirmed', 'Checkout');
$orderBody = translate('Your order {id} ships on {date}.', 'Checkout', [
    'id' => '48213', // a string, so it skips number formatting
    'date' => new DateTimeImmutable('2026-08-15'), // locale-formatted
]);
?>
<!doctype html>
<html lang="<?= $active ?>" data-demo-dir="<?= demo_dir() ?>">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Langsys × PHP — demo</title>
    <link rel="stylesheet" href="demo.css">
</head>
<body>
    <?php if ($banner): ?>
        <div class="demo-banner" translate="no">
            <strong>Shared demo project (read-only)</strong> — existing phrases translate, but a read-only key can't add new ones. To watch a phrase you write get translated, <a href="https://github.com/langsys/langsys-demos/tree/main/php#use-your-own-project" target="_blank" rel="noopener noreferrer">run this app on your own project</a> or <a href="https://docs.langsys.dev/learn/quickstart" target="_blank" rel="noopener noreferrer">see it in the quickstart video</a>.
            <a href="https://docs.langsys.dev/learn/concepts/keys-and-environments" target="_blank"
                rel="noopener noreferrer">Get your keys</a>
        </div>
    <?php endif ?>

    <div class="app">
        <header class="topbar">
            <div class="brand">
                <span class="logo">◆</span> <span translate="no">Langsys</span> × PHP
            </div>
            <!-- Server-rendered language picker: a GET form, so ?locale= reloads the page in that language
                 (the helper saves it in a cookie). Only the languages the project serves are listed. -->
            <form class="locale-form" method="get" translate="no">
                <input type="hidden" name="count" value="<?= $count ?>">
                <select class="locale-select" name="locale" aria-label="Language" onchange="this.form.submit()">
                    <?php foreach (demo_languages() as $code => $label): ?>
                        <option value="<?= $code ?>"<?= $active === $code ? ' selected' : '' ?>><?= $label ?></option>
                    <?php endforeach ?>
                </select>
                <noscript><button type="submit">Go</button></noscript>
            </form>
        </header>

        <section class="card">
            <h2><code>t()</code> — inline string, in a template</h2>
            <pre class="call"><code><?= htmlspecialchars(CODE['greeting']) ?></code></pre>
            <div class="live">
                <p><?= t('Hello, {name}!', 'Greetings', ['name' => 'Sarah']) ?></p>
            </div>
        </section>

        <section class="card">
            <h2><code>t()</code> — plurals, written flat</h2>
            <pre class="call"><code><?= htmlspecialchars(CODE['plural']) ?></code></pre>
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
            <pre class="call"><code><?= htmlspecialchars(CODE['order']) ?></code></pre>
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
            <pre class="call"><code><?= htmlspecialchars(CODE['categories']) ?></code></pre>
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
            <pre class="call"><code><?= htmlspecialchars(CODE['coverage']) ?></code></pre>
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
