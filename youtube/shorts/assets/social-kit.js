/* ──────────────────────────────────────────────────────────────────────────
   Langsys social demo kit — shared frame engine.

   Every demo is frame-addressed: renderFrame(f) fully describes the stage for
   frame f, with no running animation and no timing races. That is what lets a
   capture script screenshot `?frame=N` for N in 0..TOTAL-1 and get a
   reproducible sequence.

   Query params
     ?frame=N     freeze on one frame (capture mode)
     ?ratio=1x1   render the 1080×1080 cut instead of 1080×1350
     ?ratio=9x16  render the 1080×1920 YouTube Shorts cut

   Usage — a demo supplies its scenes and a render callback:

     LangsysDemo({
       fps: 4,
       seconds: 12,
       outro: 'closing copy',
       scenes: [
         { until: 3.0, locale: 'es', caption: '…', … },
         { until: 12.0, outro: true },
       ],
       render(scene, ctx) { … },
     });

   The kit handles the frame math, the progress bar, the locale pills, the
   caption line and the outro card. Everything a scene means beyond that is the
   demo's own business — it reads whatever extra fields it put on the scene.
   ────────────────────────────────────────────────────────────────────────── */

window.LangsysDemo = function (config) {
    const { fps, seconds, scenes, outro, render } = config;
    const TOTAL = fps * seconds;

    const el = (id) => document.getElementById(id);
    const params = new URLSearchParams(location.search);

    if (params.get('ratio') === '1x1') el('stage').classList.add('r1x1');
    if (params.get('ratio') === '9x16') el('stage').classList.add('r9x16');

    function sceneAt(second) {
        for (const s of scenes) if (second < s.until) return s;
        return scenes[scenes.length - 1];
    }

    function setLocale(locale) {
        for (const pill of document.querySelectorAll('.pill')) {
            pill.classList.toggle('on', pill.dataset.loc === locale);
        }
    }

    // Tint the ICU branch that actually fired, so the rendered sentence and the
    // stored catalog entry are visibly the same object.
    //
    // The inner (?:[^{}]|\{[^{}]*\})* allows one level of nesting, because a
    // select branch usually contains a placeholder of its own —
    // `male {¡Bienvenido, {name}!}`. A flat [^{}]* stops at that inner brace
    // and silently highlights nothing.
    //
    // \b matters too: it keeps the `male` category from matching inside
    // `female {…}`, since the preceding `e` is a word character.
    function highlightBranch(icu, category) {
        const escaped = icu.replace(/&/g, '&amp;').replace(/</g, '&lt;');
        if (!category) return escaped;
        const re = new RegExp('(\\b' + category + ' \\{(?:[^{}]|\\{[^{}]*\\})*\\})');
        return escaped.replace(re, '<span class="hl">$1</span>');
    }

    function renderFrame(f) {
        const frame = Math.max(0, Math.min(TOTAL - 1, f));
        const scene = sceneAt(frame / fps);

        el('progress').style.width = ((frame + 1) / TOTAL * 100) + '%';

        if (scene.outro) {
            el('outro').classList.add('on');
            el('outroLine').innerHTML = outro;
            return;
        }
        el('outro').classList.remove('on');

        if (el('caption')) el('caption').innerHTML = scene.caption || '';
        if (scene.locale) setLocale(scene.locale);

        render(scene, { el, frame, second: frame / fps, highlightBranch });
    }

    window.renderFrame = renderFrame;
    window.TOTAL_FRAMES = TOTAL;

    const requested = params.get('frame');
    if (requested !== null) {
        renderFrame(parseInt(requested, 10));
    } else {
        let f = 0;
        renderFrame(f);
        setInterval(() => renderFrame(f = (f + 1) % TOTAL), 1000 / fps);
    }
};
