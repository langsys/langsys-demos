import HoodDemo from './HoodDemo.jsx';
import { demoBanner } from './langsys';

const KEYS_URL = 'https://docs.langsys.dev/learn/concepts/keys-and-environments';

export default function App() {
    return (
        <>
            {demoBanner && (
                <div className="demo-banner" translate="no">
                    {demoBanner === 'shared' ? (
                        <>
                            <strong>Shared demo project (read-only)</strong> — existing phrases translate; new or
                            edited ones won't. Drop your own keys in <code>.env</code> to watch discovery register and
                            translate your phrases live.
                        </>
                    ) : (
                        <>
                            <strong>No Langsys credentials configured</strong> — showing source text only, nothing
                            translates. Add your project id and key in <code>.env</code> to see it live.
                        </>
                    )}{' '}
                    <a href={KEYS_URL} target="_blank" rel="noopener noreferrer">
                        Get your keys →
                    </a>
                </div>
            )}
            <HoodDemo />
        </>
    );
}
