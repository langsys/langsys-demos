// app/layout.jsx (Server Component) — step 1 of docs.langsys.dev/learn/guides/nextjs:
// fetch the catalog on the server with a raw fetch, hand it to the client wrapper.
import { cookies } from 'next/headers';
import { LangsysClient } from './LangsysClient';
import { DEMO_KEY, DEMO_PROJECT_ID, LOCALES, LOCALE_COOKIE } from './langsys';
import './demo.css';

export const metadata = { title: 'Langsys × Next.js — demo' };

// Your own credentials from .env.local, else the shared read-only demo project. The server key may
// be a WRITE key — it never leaves the server. The client only ever gets the read-only one.
const projectId = process.env.LANGSYS_PROJECT_ID || DEMO_PROJECT_ID;
const serverKey = process.env.LANGSYS_API_KEY || DEMO_KEY;
const clientKey = process.env.NEXT_PUBLIC_LANGSYS_API_KEY || DEMO_KEY;
const apiUrl = process.env.NEXT_PUBLIC_LANGSYS_API_URL || 'https://api.langsys.dev/api';

async function getTranslations(locale) {
    const res = await fetch(`${apiUrl}/projects/${projectId}/translations?locale=${locale}`, {
        headers: { 'x-Authorization': serverKey },
        cache: 'no-store',
    });
    // No catalog (bad key, API down): render the source text rather than fail the page.
    if (!res.ok) return {};
    const result = await res.json();
    return result.data ?? {};
}

export default async function RootLayout({ children }) {
    // From the cookie the locale switcher writes; a first visit gets English.
    const saved = (await cookies()).get(LOCALE_COOKIE)?.value;
    const locale = LOCALES.includes(saved) ? saved : 'en-US';
    const translations = await getTranslations(locale);

    return (
        <html lang={locale}>
            <body>
                <LangsysClient
                    locale={locale}
                    translations={translations}
                    projectId={projectId}
                    apiKey={clientKey} // read-only
                    apiUrl={process.env.NEXT_PUBLIC_LANGSYS_API_URL}
                    banner={process.env.LANGSYS_PROJECT_ID ? null : 'shared'}
                >
                    {children}
                </LangsysClient>
            </body>
        </html>
    );
}
