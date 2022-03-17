<template>
  <div>
    <div
      class="grid grid-cols-1 gap-4 mt-10 px-5 sm:grid-cols-2 max-w-5xl mx-auto"
    >
      <div class="bg-violet-200 rounded-xl p-3 shadow-xl">
        <FileUpload></FileUpload>
      </div>
      <VideoResult></VideoResult>
    </div>

    <PictureThumbnail></PictureThumbnail>
  </div>
</template>

<script setup>
import PictureThumbnail from "@/components/home/PictureThumbnail.vue";
import FileUpload from "@/components/home/FileUpload.vue";
import VideoResult from "@/components/home/VideoResult.vue";
</script>
