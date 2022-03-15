<template>
  <div class="grid grid-cols-1 gap-4 mt-10 px-5 sm:grid-cols-2">
    <FileUpload></FileUpload>

    <VideoResult></VideoResult>
  </div>
  <div class="grid grid-cols-1 gap-4 mt-10 px-5 sm:grid-cols-2">
    <AdvancedOptions></AdvancedOptions>
    <div class="bg-blue-200 rounded-xl">hjælp</div>
  </div>
</template>

<script>
import FileUpload from "@/components/home/FileUpload.vue";
import AdvancedOptions from "@/components/home/AdvancedOptions.vue";
import VideoResult from "@/components/home/VideoResult.vue";
export default {
  components: {
    FileUpload,
    AdvancedOptions,
    VideoResult,
  },
};
</script>
