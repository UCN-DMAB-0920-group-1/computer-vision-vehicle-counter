<template>
  <div>
    <div
      class="grid grid-cols-1 gap-4 mt-10 sm:grid-cols-2 max-w-5xl mx-auto"
    >
      <div class="bg-violet-200 rounded-xl p-3 shadow-xl">
        <FileUpload></FileUpload>
        <div v-if="videoUrl" class="">
          <PictureThumbnail></PictureThumbnail>
        </div>
      </div>
          <VideoResult></VideoResult>
    </div>

  </div>
</template>

<script setup>
import PictureThumbnail from "@/components/home/PictureThumbnail.vue";
import FileUpload from "@/components/home/FileUpload.vue";
import VideoResult from "@/components/home/VideoResult.vue";
import {useStore} from "vuex"
import { computed } from "vue";
const store = useStore();
let videoUrl = computed(() => store.getters["FileProcessing/videoUrl"])
</script>
