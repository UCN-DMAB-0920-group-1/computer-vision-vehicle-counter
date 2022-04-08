<template>
  <div class="rounded-lg p-3 sm:w-80 w-[95%] mx-auto">
    <p class="text-left" v-for="entity in Object.entries(props.video)" :key="entity[0]">
      <span class="font-semibold">{{ entity[0] }}:</span>: {{ entity[1] }}
    </p>

    <button
    v-if="props.video.status === 'Done'"
      @click="downloadVideo"
      :class="props.video.status"
      class="mx-auto px-3 shadow-xl block rounded-full bg-violet-700 p-2 text-white mt-4 transition ease-in-out hover:text-violet-500 hover:bg-white font-semibold"
    >
      Download video
    </button>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
const props = defineProps(["video"]);

function downloadVideo() {
  const id = props.video._id;
  //
  const a = Object.assign(document.createElement("a"), {
    href: "data:process.env.VUE_APP_PROCESSING_ENDPOINT" + "detection/" + id + "/video",
    style: "display:none",
    download: "ML-Tacking-" + id,
  });
  document.appendChild(a);
  a.click();
  a.remove();
}
</script>

<style scoped></style>
