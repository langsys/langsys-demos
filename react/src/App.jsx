import { useState } from 'react';
import HoodDemo from './HoodDemo.jsx';
import StoreDemo from './StoreDemo.jsx';

// PROTOTYPE: a floating switch to compare the two demo directions live.
// (Temporary — the final demo will render just one of them.)
const switchStyle = {
    position: 'fixed',
    right: 12,
    bottom: 12,
    zIndex: 100,
    display: 'flex',
    gap: 4,
    padding: 4,
    borderRadius: 999,
    background: 'rgba(20,21,42,0.9)',
    boxShadow: '0 6px 20px rgba(0,0,0,0.3)',
    fontFamily: 'system-ui, sans-serif',
    fontSize: 12,
};

function SwitchButton({ active, onClick, children }) {
    return (
        <button
            onClick={onClick}
            style={{
                border: 'none',
                cursor: 'pointer',
                borderRadius: 999,
                padding: '5px 12px',
                fontWeight: 600,
                color: active ? '#14152a' : '#c9cbe6',
                background: active ? '#fff' : 'transparent',
            }}
        >
            {children}
        </button>
    );
}

export default function App() {
    const [demo, setDemo] = useState('hood');

    return (
        <>
            {demo === 'hood' ? <HoodDemo /> : <StoreDemo />}
            <div style={switchStyle}>
                <SwitchButton active={demo === 'hood'} onClick={() => setDemo('hood')}>
                    Under the hood
                </SwitchButton>
                <SwitchButton active={demo === 'store'} onClick={() => setDemo('store')}>
                    Store
                </SwitchButton>
            </div>
        </>
    );
}
