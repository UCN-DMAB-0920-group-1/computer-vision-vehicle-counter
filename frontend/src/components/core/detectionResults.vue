<template>
    <div class=" bg-violet-300 rounded-lg p-3 shadow-md">
        <h1 class="font-bold text-lg">Video result ({{  }})</h1>
        <p class="text-left" v-for="entity in Object.entries(videoData)" :key="entity[0]"><span class="font-semibold ">{{ entity[0] }}:</span>: {{ entity[1] }}</p>
    </div>
</template>

<script setup>
const props = defineProps(['video'])


</script>

<style lang="scss" scoped>

</style>