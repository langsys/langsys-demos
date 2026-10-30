<?php

use Illuminate\Support\Facades\Route;
use Langsys\Laravel\LangsysTranslator;

Route::get('/', function (LangsysTranslator $langsys) {
    $count = max(0, min(99, (int) request()->query('count', 3)));

    // The 18 languages Langsys supports on its own surfaces, each named in
    // itself. The picker offers the ones the project serves, on the locale it
    // serves each from. Asking for a locale the project doesn't serve leaves
    // the page in English.
    $languages = [
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
    $languageOf = fn (string $code) => strtolower(explode('-', str_replace('_', '-', $code))[0]);
    // "es-419" / "zh-hans" / "pt-br" → "es-419" / "zh-Hans" / "pt-BR".
    $canonical = function (string $code): string {
        $parts = explode('-', str_replace('_', '-', $code));
        foreach ($parts as $i => $part) {
            $parts[$i] = $i === 0 ? strtolower($part) : (strlen($part) === 4 ? ucfirst(strtolower($part)) : strtoupper($part));
        }

        return implode('-', $parts);
    };

    // What the project serves — the SDK caches the project, so this costs no
    // request per page. Unreachable: offer every language rather than fail.
    try {
        $project = $langsys->client()->getProject();
    } catch (Throwable $e) {
        $project = null;
    }
    $locales = $languages;
    if (! empty($project['base_locale'])) {
        $served = ($project['default_locales'] ?? []) + [$languageOf($project['base_locale']) => $project['base_locale']];
        $locales = [];
        foreach ($languages as $code => $label) {
            if (isset($served[$languageOf($code)])) {
                $locales[$canonical($served[$languageOf($code)])] = $label;
            }
        }
    }

    // DetectLocale already ran: ?locale= / cookie / session / Accept-Language
    // resolved into app()->getLocale(). Snap it to the offered locale in the
    // same language ('es' and 'es-MX' both → 'es-419'), or English when the
    // project doesn't serve that language. t() and @t read the app locale.
    $active = collect(array_keys($locales))
        ->first(fn (string $code) => $languageOf($code) === $languageOf(app()->getLocale())) ?? 'en-US';
    app()->setLocale($active);

    // Which banner the page shows: null when the visitor supplied their own
    // .env credentials, 'shared' on the public read-only demo project (the
    // fallback in config/langsys.php), 'unconfigured' when neither exists.
    $banner = env('LANGSYS_PROJECT_ID') ? null : (config('langsys.project_id') ? 'shared' : 'unconfigured');

    return view('demo', [
        'count' => $count,
        'locales' => $locales,
        'active' => $active,
        'dir' => $languageOf($active) === 'ar' ? 'rtl' : 'ltr',
        'banner' => $banner,
        // t() works anywhere in PHP — controllers, Livewire, jobs, mail.
        // Computed here so the card shows a server-side result, not a directive.
        'orderTitle' => t('Order confirmed', 'Checkout'),
        'orderBody' => t('Your order {id} ships on {date}.', 'Checkout', [
            'id' => '48213', // a string, so it skips number formatting
            'date' => new DateTimeImmutable('2026-08-15'), // locale-formatted
        ]),
    ]);
});
