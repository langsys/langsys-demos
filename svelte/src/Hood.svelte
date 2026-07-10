<script>
    let { code, children } = $props();
</script>

<div class="hood">
    <div class="hood-code">
        <div class="chrome">
            <span class="dot"></span> <span class="dot"></span> <span class="dot"></span>
            <span class="chrome-name">App.svelte</span>
        </div>
        <pre><code>{code}</code></pre>
    </div>
    <div class="hood-arrow">renders ↓</div>
    <div class="hood-render">
        <div class="chrome browser">
            <span class="dot"></span> <span class="dot"></span> <span class="dot"></span>
            <span class="chrome-name">live</span>
        </div>
        <div class="hood-output">{@render children()}</div>
    </div>
</div>
