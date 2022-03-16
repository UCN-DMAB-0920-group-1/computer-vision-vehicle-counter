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
    <section class="bg-blue-200 rounded-xl p-3" v-else>
      <h1 class="font-bold text-lg">Upload video {{ loading }}</h1>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illum sint
        accusamus aliquam commodi quisquam beatae tempore vitae quo iste sit!
        Cumque ducimus distinctio pariatur doloremque reiciendis repellat amet
        sed iste?
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
      <p>{{ error }}</p>
    </section>
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
      if (!file.value) {
        error.value = "Please select a file!";

        return;
      }

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
      loading,
      error,
    };
  },
};
</script>
