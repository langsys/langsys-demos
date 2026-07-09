import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './langsys'; // initializes Langsys (side effect)
import App from './App.jsx';

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <App />
    </StrictMode>,
);
