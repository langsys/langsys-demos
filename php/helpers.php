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

// The 18 languages Langsys supports on its own surfaces, each named in itself. The picker offers
// the ones the project serves, on the locale it serves each from (demo_languages()). Asking for a
// locale the project doesn't serve leaves the page in English.
const LANGUAGES = [
    'en-US' => 'English',
    'es-419' => 'Español',
    'pt-BR' => 'Português',
    'fr-FR' => 'Français',
    'de-DE' => 'Deutsch',
    'it-IT' => 'Italiano',
    'ja-JP' => '日本語',
    'zh-Hans' => '中文',
    'ko-KR' => '한국어',
    'ru-RU' => 'Русский',
    'uk-UA' => 'Українська',
    'tr-TR' => 'Türkçe',
    'pl-PL' => 'Polski',
    'nl-NL' => 'Nederlands',
    'id-ID' => 'Bahasa Indonesia',
    'vi-VN' => 'Tiếng Việt',
    'hi-IN' => 'हिन्दी',
    'ar-001' => 'العربية',
];

const RTL_LANGUAGES = ['ar'];

function language_of(string $code): string
{
    return strtolower(explode('-', str_replace('_', '-', $code))[0]);
}

/** The one client for this request. Your own credentials from the environment, else the shared demo. */
function langsys(): Client
{
    static $langsys = null;

    return $langsys ??= new Client(
        getenv('LANGSYS_API_KEY') ?: DEMO_KEY,
        getenv('LANGSYS_PROJECT_ID') ?: DEMO_PROJECT_ID,
        array_filter(['api_url' => getenv('LANGSYS_API_URL') ?: null]),
    );
}

/**
 * The languages the project serves, as [locale => name], each on the locale the project serves it
 * from. The client caches the project (an hour, by default), so this costs no request per page.
 */
function demo_languages(): array
{
    static $offered = null;
    if ($offered !== null) {
        return $offered;
    }

    try {
        $project = langsys()->getProject();
    } catch (Throwable $e) {
        $project = null; // Unreachable: offer every language rather than fail the page.
    }
    if (empty($project['base_locale'])) {
        return $offered = LANGUAGES;
    }

    $served = ($project['default_locales'] ?? []) + [language_of($project['base_locale']) => $project['base_locale']];
    $offered = [];
    foreach (LANGUAGES as $code => $label) {
        if (isset($served[language_of($code)])) {
            $offered[canonical_locale($served[language_of($code)])] = $label;
        }
    }

    return $offered;
}

/** "es-419" / "zh-hans" / "pt-br" → "es-419" / "zh-Hans" / "pt-BR". */
function canonical_locale(string $code): string
{
    $parts = explode('-', str_replace('_', '-', $code));
    foreach ($parts as $i => $part) {
        $parts[$i] = $i === 0 ? strtolower($part) : (strlen($part) === 4 ? ucfirst(strtolower($part)) : strtoupper($part));
    }

    return implode('-', $parts);
}

/**
 * The visitor's locale: an explicit ?locale= (saved in a cookie so navigation keeps it), else the
 * cookie, else the browser's Accept-Language — in a language the project serves, or English.
 */
function demo_locale(): string
{
    static $locale = null;
    if ($locale !== null) {
        return $locale;
    }

    // The offered locale in the same language as $code, if any ('es' and 'es-MX' both → 'es-419').
    $pick = function (?string $code): ?string {
        foreach (array_keys(demo_languages()) as $offered) {
            if ($code && language_of($offered) === language_of($code)) {
                return $offered;
            }
        }
        return null;
    };

    $locale = $pick($_GET['locale'] ?? null);
    if ($locale !== null) {
        setcookie('langsys_locale', $locale, ['expires' => time() + 31536000, 'path' => '/', 'samesite' => 'Lax']);
    } else {
        $detected = LocaleDetector::fromAcceptLanguage($_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? '');
        $locale = $pick($_COOKIE['langsys_locale'] ?? null) ?? $pick($detected) ?? 'en-US';
    }
    langsys()->setLocale($locale);

    return $locale;
}

/** 'rtl' for a right-to-left language, so the page lays its translated output out that way. */
function demo_dir(): string
{
    return in_array(language_of(demo_locale()), RTL_LANGUAGES, true) ? 'rtl' : 'ltr';
}

/**
 * Translate, falling back to the phrase itself. langsys-php 1.3.1 returns null for a phrase the
 * project has but hasn't translated into this locale yet (a language just added, say), so the
 * fallback is ours: the base phrase, with its values still filled in.
 */
function translate(string $phrase, string $category, array $params = []): string
{
    return langsys()->translate($phrase, demo_locale(), $category, null, $params)
        ?? langsys()->getInterpolator()->interpolate($phrase, $params, demo_locale());
}

/** Translate and escape, for templates. */
function t(string $phrase, string $category, array $params = []): string
{
    return htmlspecialchars(translate($phrase, $category, $params));
}
