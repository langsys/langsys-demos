// The blog's CMS, in the browser: posts live in localStorage, so the admin page
// and the post page share them without a server. Publishing is the only write;
// nothing here knows about Langsys.

export interface Post {
    slug: string;
    title: string;
    body: string[];
    published: string;
}

const STORE = 'selvara-journal-posts';

// The draft the admin page opens on, so a take types a title rather than a
// whole article.
export const DRAFT: Omit<Post, 'slug' | 'published'> = {
    title: 'How we dye our linen with avocado pits',
    body: [
        'Every bedspread in our autumn collection takes its color from the avocado pits our neighbors save for us.',
        'We simmer them for six hours, and the water turns a soft, dusty pink that no two batches repeat.',
        'The linen is washed twice before it ships, so the color stays in the cloth and out of your laundry.',
    ],
};

export function allPosts(): Post[] {
    try {
        return JSON.parse(localStorage.getItem(STORE) ?? '[]') as Post[];
    } catch {
        return [];
    }
}

export function findPost(slug: string): Post | undefined {
    return allPosts().find((post) => post.slug === slug);
}

export function slugify(title: string): string {
    return title
        .toLowerCase()
        .normalize('NFKD')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '');
}

export function publish(title: string, body: string[]): Post {
    const post: Post = { slug: slugify(title), title, body, published: new Date().toISOString() };
    const others = allPosts().filter((existing) => existing.slug !== post.slug);
    localStorage.setItem(STORE, JSON.stringify([post, ...others]));
    return post;
}

export function formatDate(iso: string): string {
    return new Date(iso).toLocaleString('en-US', { month: 'long', day: 'numeric', hour: 'numeric', minute: '2-digit' });
}
