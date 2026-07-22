import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [vue()],
    // Pre-bundle the SDK at server start. Without this, Vite optimizes it
    // mid-first-load and fires a reload StackBlitz's preview can miss,
    // leaving the app stuck until a manual refresh.
    optimizeDeps: {
        include: ['langsys-js-vue'],
    },
});
