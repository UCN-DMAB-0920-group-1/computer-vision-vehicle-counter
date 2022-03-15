<template>
  <div class="bg-blue-200 rounded-xl p-3">
    <h1>Upload video</h1>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illum sint
      accusamus aliquam commodi quisquam beatae tempore vitae quo iste sit!
      Cumque ducimus distinctio pariatur doloremque reiciendis repellat amet sed
      iste?
    </p>
    <input
      class="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
      type="file"
      @change="onFileChange"
    />
    <button
      class="block w-full rounded-full bg-blue-300 p-2 text-white mt-4"
      @click="onUploadFile"
    >
      Upload
    </button>
  </div>
</template>

<script>
import { ref } from "vue";
import { useStore } from "vuex";
export default {
  setup() {
    const store = useStore();

    let file = ref("");
    let error = ref("");
    let loading = ref(false);

    function onFileChange(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;

      error.value = "";
      file.value = files[0];
    }

    async function onUploadFile() {
      if (!this.file) error.value = "Please select a file";

      try {
        loading.value = true;
        store.dispatch("FileProcessing/uploadVideo", file.value);
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
    };
  },
};
</script>
