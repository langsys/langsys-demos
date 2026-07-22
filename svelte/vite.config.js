import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
    plugins: [svelte()],
    // Pre-bundle the SDK at server start. Without this, Vite optimizes it
    // mid-first-load and fires a reload StackBlitz's preview can miss,
    // leaving the app stuck until a manual refresh.
    optimizeDeps: {
        include: ['langsys-js-svelte'],
    },
});
