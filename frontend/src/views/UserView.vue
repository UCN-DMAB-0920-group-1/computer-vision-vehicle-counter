<template>
  <div>
    <div v-if="loggedIn" class="flex gap-5 flex-wrap w-full justify-center">
      <div class="bg-violet-300 shadow-md rounded-lg" v-for="video in videos" :key="video.UUID">
        <DetectionResults :video="video"></DetectionResults>
      </div>
    </div>

    <LoginText v-else></LoginText>
  </div>
</template>

<script setup>
import DetectionResults from "@/components/core/detectionResults.vue";
import LoginText from "@/components/home/LoginText.vue";

import { computed } from "vue";
import { useStore } from "vuex";
const store = useStore();
let loggedIn = computed(() => store.getters["Authorization/loginState"]);

store.dispatch("Detections/downloadUserDetections");

let videos = computed(() => store.getters["Detections/userVideos"]);
</script>

<style lang="scss" scoped></style>
