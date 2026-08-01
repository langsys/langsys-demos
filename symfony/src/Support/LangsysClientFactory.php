<?php

namespace App\Support;

use Langsys\SDK\Cache\CacheInterface;
use Langsys\SDK\Client;

/**
 * Demo-only client construction, mirroring the Laravel demo's
 * config/langsys.php (shared read-only fallback) + AppServiceProvider
 * (offline stand-in). The `?:` fallbacks treat empty .env values as unset,
 * so a fresh clone runs on the shared demo project out of the box.
 */
class LangsysClientFactory
{
    // Shared public demo project — READ-ONLY key, fixed pre-translated catalog.
    // Safe to publish: it can only fetch translations, never register or spend.
    // Changing these? The other demos keep their copies in src/langsys.js/.ts
    // and laravel/config/langsys.php — all copies must match.
    private const SHARED_PROJECT_ID = '90455431-01d4-47c5-acb8-4fb4fdc6b4f4';
    private const SHARED_KEY = 'vAgxOao966WHaxApSBwaLwRlWwZMABmLNHmayhpbAt7JqIpYcybGKms5VGoQ27O0';

    public static function create(CacheInterface $cache): Client
    {
        $apiKey = self::env('LANGSYS_API_KEY') ?: self::SHARED_KEY;
        $projectId = self::env('LANGSYS_PROJECT_ID') ?: self::SHARED_PROJECT_ID;

        // With no credentials the real SDK client refuses to construct; swap
        // in the offline stand-in so the demo renders source text (and shows
        // its "unconfigured" banner) instead of throwing.
        if (!$apiKey || !$projectId) {
            return new OfflineClient();
        }

        return new Client($apiKey, $projectId, [
            'api_url' => self::env('LANGSYS_API_URL') ?: 'https://api.langsys.dev/api',
            'cache' => $cache,
        ]);
    }

    /**
     * Which banner the page shows: null when the visitor supplied their own
     * .env credentials, 'shared' on the public read-only demo project,
     * 'unconfigured' when neither exists.
     */
    public static function bannerState(): ?string
    {
        if (self::env('LANGSYS_PROJECT_ID')) {
            return null;
        }

        return self::SHARED_PROJECT_ID !== '' ? 'shared' : 'unconfigured';
    }

    private static function env(string $name): string
    {
        return (string) ($_ENV[$name] ?? $_SERVER[$name] ?? getenv($name) ?: '');
    }
}
