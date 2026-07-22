import { defineConfig } from 'vite';

export default defineConfig({
    // Pre-bundle the SDK at server start. Without this, Vite optimizes it
    // mid-first-load and fires a reload StackBlitz's preview can miss,
    // leaving the app stuck until a manual refresh.
    optimizeDeps: {
        include: ['langsys-js-typescript'],
    },
});
