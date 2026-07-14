import HoodDemo from './HoodDemo.jsx';
import { isSharedDemo } from './langsys';

export default function App() {
    return (
        <>
            {isSharedDemo && (
                <div className="demo-banner" translate="no">
                    <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or edited ones
                    won't. Drop your own keys in <code>.env</code> to watch discovery register and translate your
                    phrases live.{' '}
                    <a
                        href="https://docs.langsys.dev/learn/concepts/keys-and-environments"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Get your keys →
                    </a>
                </div>
            )}
            <HoodDemo />
        </>
    );
}
