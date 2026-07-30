import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

// The preset aliases react / react-dom / react-dom/client → preact/compat and
// wires Preact's JSX transform, so the app consumes langsys-js-react (and the
// verbatim React demo code) with no changes.
export default defineConfig({
    plugins: [preact()],
    // Pre-bundle the SDK at server start. Without this, Vite optimizes it
    // mid-first-load and fires a reload StackBlitz's preview can miss,
    // leaving the app stuck until a manual refresh.
    optimizeDeps: {
        include: ['langsys-js-react'],
    },
});
