import { resolve } from 'node:path';
import { defineConfig } from 'vite';

export default defineConfig({
    optimizeDeps: {
        include: ['langsys-js-typescript'],
    },
    build: {
        rollupOptions: {
            input: {
                index: resolve(__dirname, 'index.html'),
                post: resolve(__dirname, 'post.html'),
                admin: resolve(__dirname, 'admin.html'),
            },
        },
    },
});
