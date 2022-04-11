<template>
  <div>
    <section class="p-2">
      <h1 class="font-bold text-lg p-2">Upload video</h1>

      <label class="m-2 w-full">Advanced Options</label>
      <input
        class="text-violet-700 rounded-md focus:ring-violet-300"
        type="checkbox"
        v-model="advancedOptions.enabled"
      />
      <section class="w-full mt-2 bg-violet-400 rounded-xl p-4 shadow-xl" v-if="advancedOptions.enabled">
        <div
          class="px-1 w-max mx-auto shadow-md text-violet-700 mb-3 text-center font-bold border-1 rounded-lg bg-white"
        >
          <label class="m-2">Draw your own ROI</label>
          <input
            type="checkbox"
            class="text-violet-700 rounded-md focus:ring-violet-300"
            v-model="advancedOptions.drawBoundingBox"
          />
        </div>
        <div
          v-if="!advancedOptions.drawBoundingBox"
          class="grid grid-cols-1 gap-2 mb-2 sm:grid-cols-2 bg-violet-800 rounded-lg p-4"
        >
          <div>
            <label class="text-white text-center font-bold">start X:</label>
            <input
              v-model="bboxCoordinates.startX"
              class="w-full rounded-md border-violet-300 text-violet-700 font-bold"
              type="number"
              name="startX"
            />
          </div>
          <div>
            <label class="text-white text-center font-bold">end X:</label>
            <input
              v-model="bboxCoordinates.endX"
              class="w-full rounded-md border-violet-300 text-violet-700 font-bold"
              type="number"
              name="endX"
            />
          </div>
          <div>
            <label class="text-white text-center font-bold">start Y:</label>
            <input
              v-model="bboxCoordinates.startY"
              class="w-full rounded-md border-violet-300 text-violet-700 font-bold"
              type="number"
              name="startY"
            />
          </div>
          <div>
            <label class="text-white text-center font-bold">end Y:</label>
            <input
              v-model="bboxCoordinates.endY"
              class="w-full rounded-md border-violet-300 text-violet-700 font-bold"
              type="number"
              name="endY"
            />
          </div>
        </div>
        <div v-if="videoUrl" class="my-2">
          <PictureThumbnail></PictureThumbnail>
        </div>
        <div class="my-4 mt-6 w-full">
          <label class="text-violet-700 shadow-md m-1 p-1 text-center font-bold border-1 rounded-lg bg-white"
            >Confidence: {{ advancedOptions.confidence }}%</label
          >
          <input
            v-model="advancedOptions.confidence"
            type="range"
            name="range"
            class="w-full h-1 shadow-xl bg-blue-100 appearance-none rounded-lg"
          />
        </div>

        <div class="my-2">
          <label class="text-white font-bold">Max Distance Between Trackings:</label>
          <br />
          <input
            v-model="advancedOptions.maxDistanceBetweenPoints"
            class="w-1/2 mx-auto text-center rounded-md border-violet-300 text-violet-700 font-bold"
            type="number"
            name="startX"
          />
        </div>
      </section>

      <div class="mx-auto">
        <input
          class="text-slate-500 file:m-4 file:shadow-md file:px-4 file:py-2 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:text-violet-50 hover:file:bg-violet-700 file:transition ease-in-out"
          type="file"
          @change="onFileChange"
        />
      </div>
      <button
        v-if="loading"
        class="shadow-xl block w-full rounded-full bg-violet-700 p-2 text-white mt-4 transition ease-in-out hover:text-violet-700 hover:bg-white font-semibold"
      >
        <div v-if="loading" class="flex justify-center items-center">
          <div class="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full" role="status">
            <span >¤ </span>
          </div>
          <p class="px-2"> Loading...</p>
        </div>
      </button>
      <button
        v-else
        class="shadow-xl block mx-auto px-5 rounded-full bg-violet-700 p-2 text-white mt-4 transition ease-in-out hover:text-violet-700 hover:bg-white font-semibold"
        @click="onUploadFile"
      >
        Upload
      </button>
    </section>
  </div>
      <div class="fixed bottom-6 z-10 flex flex-col justify-end flex-wrap h-full pt-6 gap-3">
        <div v-for="item in error" :key="item">
          <AlertPopup :text="item" :type="'Warning'"></AlertPopup>
        </div>
      </div>
</template>

<script>
import { ref, watch, computed } from "vue";
import { useStore } from "vuex";
import PictureThumbnail from "./PictureThumbnail.vue";
import AlertPopup from "../core/AlertPopup.vue";

export default {
  components: { PictureThumbnail, AlertPopup },
  setup() {
    const store = useStore();

    let file = ref("");
    let error = ref([]);
    let loading = ref(false);
    let videoUrl = computed(() => store.getters["FileProcessing/videoUrl"]);


    let advancedOptions = computed(() => store.getters["FileProcessing/advancedOptions"]);

    watch(advancedOptions.value, (currentValue) => {
      store.commit("FileProcessing/saveOptions", currentValue);
    });

    let bboxCoordinates = computed(() => store.getters["FileProcessing/bboxCoordinates"]);

    watch(bboxCoordinates.value, (currentValue) => {
      store.commit("FileProcessing/saveBboxCoordinates", currentValue);
    });

    function onFileChange(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;

      file.value = files[0];
      const fileURL = URL.createObjectURL(file.value);
      store.dispatch("FileProcessing/saveVideoUrl", fileURL);
    }

    async function onUploadFile() {
      if (!file.value) {
        error.value.push("Please select a file!");
        return;
      }
      
      try {
        loading.value = true;

        const id = await store.dispatch("FileProcessing/uploadVideo", {
          file: file.value,
        });
        await store.dispatch("Detections/getVideoData", {id:id})
      } catch (e) {
        error.value.push(e);
      } finally {
        setTimeout(() => {
          loading.value = false;
        }, 2000);
      }
    }

    return {
      file: file,
      onFileChange: onFileChange,
      onUploadFile: onUploadFile,
      loading,
      error,
      advancedOptions,
      bboxCoordinates,
      videoUrl,
    };
  },
};
</script>
