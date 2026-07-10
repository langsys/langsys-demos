<script setup>
defineProps({ code: String });
</script>

<template>
    <div class="hood">
        <div class="hood-code">
            <div class="chrome">
                <span class="dot" /> <span class="dot" /> <span class="dot" />
                <span class="chrome-name">App.vue</span>
            </div>
            <pre><code>{{ code }}</code></pre>
        </div>
        <div class="hood-arrow">renders ↓</div>
        <div class="hood-render">
            <div class="chrome browser">
                <span class="dot" /> <span class="dot" /> <span class="dot" />
                <span class="chrome-name">live</span>
            </div>
            <div class="hood-output"><slot /></div>
        </div>
    </div>
</template>
