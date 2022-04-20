<template>
  <div class="rounded-lg p-3 sm:w-80 w-[95%] mx-auto">
    <div id="videoAppend"></div>
    <p class="text-left" v-for="entity in Object.entries(props.video)" :key="entity[0]">
      <span class="font-semibold">{{ entity[0] }}</span>: {{ entity[1] }}
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
import {useStore} from "vuex"
import { defineProps } from "vue";
const store = useStore();
const props = defineProps(["video"]);

async function downloadVideo() {
  const id = props.video._id;
    try {
      let url = await store.dispatch("FileProcessing/downloadVideo", id)
    if (url){
        const a = Object.assign(document.createElement("a"), {
        href: url,
        style: "display:none",
        download: "ML-Tacking" + id,
        });
        a.click();
        a.remove();
      }
    } catch (error) {
      store.dispatch("AlertsList/addAlert", {e:"Could not download file", type:"Error"});
    }
}
</script>

<style scoped></style>
