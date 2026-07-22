<script setup>
// t() — inline string, in a component (docs.langsys.dev/learn/sdk/vue).
import { useT } from 'langsys-js-vue';
const t = useT();
const name = 'Sarah';
</script>

<template>
    <p>{{ t('Hello, {name}!', 'Greetings', { name }) }}</p>
</template>
