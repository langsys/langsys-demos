<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    $count = max(0, min(99, (int) request()->query('count', 3)));

    $locales = [
        'en-US' => 'English',
        'es-ES' => 'Español',
        'fr-FR' => 'Français',
        'de-DE' => 'Deutsch',
    ];

    // DetectLocale already ran: ?locale= / cookie / session / Accept-Language
    // resolved into app()->getLocale(). Fall back to en-US for the pill state
    // when nothing matched (e.g. a first visit with an unsupported locale).
    $active = collect(array_keys($locales))
        ->first(fn (string $code) => strcasecmp($code, app()->getLocale()) === 0) ?? 'en-US';

    // Which banner the page shows: null when the visitor supplied their own
    // .env credentials, 'shared' on the public read-only demo project (the
    // fallback in config/langsys.php), 'unconfigured' when neither exists.
    $banner = env('LANGSYS_PROJECT_ID') ? null : (config('langsys.project_id') ? 'shared' : 'unconfigured');

    return view('demo', [
        'count' => $count,
        'locales' => $locales,
        'active' => $active,
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
