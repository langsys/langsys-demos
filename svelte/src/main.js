import { mount } from 'svelte';
import './demo.css';
import './langsys'; // initializes Langsys (side effect)
import App from './App.svelte';

const app = mount(App, { target: document.getElementById('app') });

export default app;
