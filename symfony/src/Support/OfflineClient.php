<?php

namespace App\Support;

use Langsys\SDK\Client;

/**
 * Stands in for the real SDK client when no credentials are configured, so
 * the demo renders source text instead of throwing (the real constructor
 * requires an api key + project id). Skips the parent constructor on
 * purpose — everything the app touches is overridden below.
 */
class OfflineClient extends Client
{
    public function __construct()
    {
    }

    public function translate($phrase, $locale = null, $category = '__uncategorized__', $contentBlockId = null)
    {
        return $phrase;
    }

    public function setLocale($locale)
    {
        return $this;
    }

    public function getLocale()
    {
        return null;
    }

    public function hasPendingRegistrations()
    {
        return false;
    }

    public function flushPendingRegistrations()
    {
        return ['phrases' => 0, 'content_blocks' => 0, 'success' => true];
    }
}
