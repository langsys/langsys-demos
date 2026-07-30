<?php

namespace App\Providers;

use App\Support\OfflineClient;
use Illuminate\Support\ServiceProvider;
use Langsys\SDK\Client;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // With no credentials the real SDK client refuses to construct; swap
        // in the offline stand-in so the demo renders source text (and shows
        // its "unconfigured" banner) instead of throwing.
        if (!config('langsys.api_key') || !config('langsys.project_id')) {
            $this->app->singleton(Client::class, fn () => new OfflineClient());
        }
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        //
    }
}
