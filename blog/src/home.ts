import { allPosts, formatDate } from './posts';
import './journal.css';

const list = document.querySelector<HTMLElement>('#posts')!;
const posts = allPosts();

if (posts.length === 0) {
    list.innerHTML = '<li class="empty">Nothing published yet. <a href="/admin.html">Write the first post</a>.</li>';
}

for (const post of posts) {
    const item = document.createElement('li');
    const link = document.createElement('a');
    link.href = `/post.html?p=${post.slug}`;
    link.textContent = post.title;
    const date = document.createElement('span');
    date.textContent = formatDate(post.published);
    item.append(link, date);
    list.append(item);
}
