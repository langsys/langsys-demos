import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import { langsys } from 'langsys-js-hono';
import { LOCALES, apiUrl, banner, key, projectid } from './langsys.config.js';
import { renderDemo } from './render.js';

const app = new Hono();

app.use(
    langsys({
        projectid,
        key, // the shared demo key is read-only; your own write key enables discovery
        apiUrl,
        baseLocale: 'en-US',
        supportedLocales: Object.keys(LOCALES),
    })
);

const css = readFileSync(join(dirname(fileURLToPath(import.meta.url)), '..', 'public', 'demo.css'), 'utf8');
app.get('/demo.css', (c) => c.text(css, 200, { 'Content-Type': 'text/css; charset=utf-8' }));

app.get('/', (c) => {
    const count = Math.max(0, Math.min(99, Number.parseInt(c.req.query('count') ?? '3', 10) || 0));
    return c.html(
        renderDemo({
            t: c.var.t,
            locale: c.var.langsysLocale,
            count,
            banner,
            framework: 'Hono',
            docsPath: 'learn/guides/node',
        })
    );
});

const port = Number.parseInt(process.env.PORT ?? '3001', 10);
serve({ fetch: app.fetch, port }, () => {
    console.log(`Langsys × Hono demo → http://localhost:${port}`);
});
