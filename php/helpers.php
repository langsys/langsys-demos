<?php

// helpers.php — the helper from docs.langsys.dev/learn/sdk/php: one client per request, one short
// name in your templates.

use Langsys\SDK\Client;
use Langsys\SDK\Locale\LocaleDetector;

// Shared public demo project — READ-ONLY key, fixed pre-translated catalog.
// Safe to publish: it can only fetch translations, never register or spend.
// Changing these? Update every copy: typescript/react/vue/svelte/preact/nextjs/nuxt/sveltekit
// (src/langsys.* or the framework's equivalent), laravel (config/langsys.php) and php (here).
const DEMO_PROJECT_ID = '90455431-01d4-47c5-acb8-4fb4fdc6b4f4';
const DEMO_KEY = 'vAgxOao966WHaxApSBwaLwRlWwZMABmLNHmayhpbAt7JqIpYcybGKms5VGoQ27O0';

const LOCALES = [
    'en-US' => 'English',
    'es-ES' => 'Español',
    'fr-FR' => 'Français',
    'de-DE' => 'Deutsch',
];

/**
 * The visitor's locale: an explicit ?locale= (saved in a cookie so navigation keeps it), else the
 * cookie, else the browser's Accept-Language — limited to the locales this demo offers.
 */
function demo_locale(): string
{
    static $locale = null;
    if ($locale !== null) {
        return $locale;
    }

    // The offered locale matching a code exactly, else one in the same language ('es' → 'es-ES').
    $pick = function (?string $code): ?string {
        if (!$code) {
            return null;
        }
        foreach ([fn ($l) => strcasecmp($l, $code) === 0, fn ($l) => strncasecmp($l, $code, 2) === 0] as $match) {
            foreach (array_keys(LOCALES) as $l) {
                if ($match($l)) {
                    return $l;
                }
            }
        }
        return null;
    };

    $locale = $pick($_GET['locale'] ?? null);
    if ($locale !== null) {
        setcookie('langsys_locale', $locale, ['expires' => time() + 31536000, 'path' => '/', 'samesite' => 'Lax']);
        return $locale;
    }

    $detected = LocaleDetector::fromAcceptLanguage($_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? '');

    return $locale = $pick($_COOKIE['langsys_locale'] ?? null) ?? $pick($detected) ?? 'en-US';
}

/** The one client for this request. Your own credentials from the environment, else the shared demo. */
function langsys(): Client
{
    static $langsys = null;

    return $langsys ??= (new Client(
        getenv('LANGSYS_API_KEY') ?: DEMO_KEY,
        getenv('LANGSYS_PROJECT_ID') ?: DEMO_PROJECT_ID,
        array_filter(['api_url' => getenv('LANGSYS_API_URL') ?: null]),
    ))->setLocale(demo_locale());
}

/** Translate and escape, for templates. */
function t(string $phrase, string $category, array $params = []): string
{
    return htmlspecialchars(langsys()->translate($phrase, null, $category, null, $params));
}
