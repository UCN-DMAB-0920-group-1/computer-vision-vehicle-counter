<template>
  <div>
    <section v-if="loading">
      <div class="flex justify-center items-center">
        <div
          class="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full"
          role="status"
        >
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </section>

    <section class="p-3" v-else>
      <h1 class="font-bold text-lg p-2">Upload video</h1>

      <label class="m-2">Advanced Options</label>
      <input type="checkbox" v-model="advancedOptions.enabled" />

      <section
        class="w-full px-6 mx-auto bg-violet-400 rounded-xl p-4 shadow-xl"
        v-if="advancedOptions.enabled"
      >
        <div class="grid grid-cols-1 gap-2 sm:grid-cols-2">
          <div>
            <label class="text-white font-bold">start X:</label>
            <input
              v-model="bboxCoordinates.startX"
              class="w-full rounded-md"
              type="number"
              name="startX"
            />
          </div>
          <div>
            <label class="text-white font-bold">end X:</label>
            <input
              v-model="bboxCoordinates.endX"
              class="w-full rounded-md"
              type="number"
              name="endX"
            />
          </div>
          <div>
            <label class="text-white font-bold">start Y:</label>
            <input
              v-model="bboxCoordinates.startY"
              class="w-full rounded-md"
              type="number"
              name="startY"
            />
          </div>
          <div>
            <label class="text-white font-bold">end Y:</label>
            <input
              v-model="bboxCoordinates.endY"
              class="w-full rounded-md"
              type="number"
              name="endY"
            />
          </div>
        </div>
        <div class="w-full mt-2">
          <label class="text-white font-bold"
            >Confidence: {{ advancedOptions.confidence }}%</label
          >
          <input
            v-model="advancedOptions.confidence"
            type="range"
            name="range"
            class="w-full h-1 shadow-xl bg-blue-100 appearance-none rounded-lg"
          />
        </div>
        <div>
          <label class="m-2">Use bounding box</label>
          <input type="checkbox" v-model="advancedOptions.drawBoundingBox" />
        </div>
      </section>

      <input
        class="text-slate-500 file:mt-3 file:shadow-xl file:px-4 file:py-2 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:text-violet-50 hover:file:bg-violet-700 file:transition ease-in-out"
        type="file"
        @change="onFileChange"
      />
      <button
        class="shadow-xl block w-full rounded-full bg-violet-700 p-2 text-white mt-4 transition ease-in-out hover:text-violet-700 hover:bg-white font-semibold"
        @click="onUploadFile"
      >
        Upload
      </button>
      <p>{{ error }}</p>
    </section>
  </div>
</template>

<script>
import { ref, watch } from "vue";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();

    let file = ref("");
    let error = ref("");
    let loading = ref(false);
    let advancedOptions = ref({
      enabled: false,
      drawBoundingBox: true,
      confidence: 0,
    });

    let bboxCoordinates = ref({
      startX: 0,
      endX: 0,
      startY: 0,
      endY: 0,
      confidence: 60,
    });

    watch(advancedOptions.value, (currentValue) => {
      store.commit("FileProcessing/saveOptions", currentValue);
    });

    watch(bboxCoordinates.value, (currentValue) => {
      store.commit("FileProcessing/saveBboxCoordinates", currentValue);
    });

    function onFileChange(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;

      error.value = "";
      file.value = files[0];

      const fileURL = URL.createObjectURL(file.value);
      store.dispatch("FileProcessing/saveVideoUrl", fileURL);
    }

    async function onUploadFile() {
      if (!file.value) {
        error.value = "Please select a file!";

        return;
      }

      try {
        loading.value = true;
        store.dispatch("FileProcessing/uploadVideo", {
          file: file.value,
        });
      } catch (e) {
        error.value = e;
      } finally {
        loading.value = false;
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
    };
  },
};
</script>
