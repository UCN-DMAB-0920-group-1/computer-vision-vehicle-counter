<template>
  <div class="rounded-lg p-3 sm:w-80 w-[95%] mx-auto">
    <div id="videoAppend"></div>
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
import { getCookie } from "@/util/Cookie";
import { defineProps } from "vue";
const props = defineProps(["video"]);

async function downloadVideo() {
  const id = props.video._id;

  const response = await fetch(`${process.env.VUE_APP_PROCESSING_ENDPOINT}/detection/${id}/video`, {
    method: "GET",
    headers: { Authorization: getCookie("jwt") },
  });

  if (response.ok) {
    const blob = await response.blob();
    let url = URL.createObjectURL(blob);

    const a = Object.assign(document.createElement("a"), {
      href: url,
      style: "display:none",
      download: "ML-Tacking" + id,
    });

    a.click();
    a.remove();
  } else {
    //TODO: show custom alert
    alert("Heyo, something went wrong while fetching the video!");
  }
}
</script>

<style scoped></style>
