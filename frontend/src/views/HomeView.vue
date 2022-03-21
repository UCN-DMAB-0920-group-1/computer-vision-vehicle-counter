<template>
  <div>
    <div
      class="grid grid-cols-1 gap-3 sm:grid-cols-2 max-w-5xl mx-auto"
    >
      <div class="bg-violet-200 rounded-xl shadow-xl">
        <FileUpload></FileUpload>
      
      </div>
          <VideoResult></VideoResult>
    </div>

  </div>
</template>

<script setup>
import FileUpload from "@/components/home/FileUpload.vue";
import VideoResult from "@/components/home/VideoResult.vue";

</script>
