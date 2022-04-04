<template>
    <div>
        {{videos}}
    </div>
</template>

<script setup>
import {computed} from "vue"
import {useStore} from "vuex"
const store = useStore()

store.dispatch("Detections/downloadUserDetections");

let videos = computed(() => store.getters["detections/userVideos"]);

</script>

<style lang="scss" scoped>

</style>