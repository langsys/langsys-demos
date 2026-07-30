<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        $middleware->web(append: [
            // Resolves ?locale= / cookie / session / Accept-Language, then
            // persists the visitor's choice — the locale pills are plain links.
            \Langsys\Laravel\Http\Middleware\DetectLocale::class,
            // After the response is sent, registers any phrases rendered for
            // the first time (write keys only; read keys skip silently).
            \Langsys\Laravel\Http\Middleware\FlushPendingRegistrations::class,
        ]);
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();
