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
      <h1 class="font-bold text-lg p-2 ">Upload video {{ loading }}</h1>

      
      <label class="m-2">Advanced Options</label>
      <input type="checkbox" v-model="advancedOptions.enabled" >
      

      <section class="w-full px-6 mx-auto bg-violet-400 rounded-xl p-4 shadow-xl" v-if="advancedOptions.enabled">
        <div class="grid grid-cols-1 gap-2 sm:grid-cols-2">
          <div>
            <label class="text-white font-bold">start X:</label>
            <input v-model="advancedOptions.startX" class="w-full rounded-md" type="number" name="startX" />
          </div>
       <div>
            <label class="text-white font-bold">end X:</label>
            <input v-model="advancedOptions.endX" class="w-full rounded-md" type="text" name="endX" />
          </div><div>
            <label class="text-white font-bold">start Y:</label>
            <input v-model="advancedOptions.startY" class="w-full rounded-md" type="number" name="startY" />
          </div><div>
            <label class="text-white font-bold">end Y:</label>
            <input v-model="advancedOptions.endY" class="w-full rounded-md" type="number" name="endY" />
          </div>
        </div>
          <div class="w-full  mt-2">
            <label class="text-white font-bold">Confidence: {{advancedOptions.confidence}}%</label>
            <input v-model="advancedOptions.confidence" type="range" name="range" class="w-full h-1 shadow-xl bg-blue-100 appearance-none rounded-lg" />
          </div>
      </section>
      <p class="m-5">
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illum sint
        accusamus aliquam commodi quisquam beatae tempore vitae quo iste sit!
        Cumque ducimus distinctio pariatur doloremque reiciendis repellat amet
        sed iste?
      </p>
      <input
        class="text-slate-500 file:shadow-xl file:px-4 file:py-2 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:text-violet-50 hover:file:bg-violet-700 file:transition ease-in-out"
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
      <canvas id="prevImgCanvas">Your browser does not support the HTML5 canvas tag.</canvas>
  </div>
</template>

<script>

import { ref} from "vue";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();

    let file = ref("");
    let error = ref("");
    let loading = ref(false);
    let advancedOptions = ref({
      enabled:false,
      startX: 0,
      endX: 0,
      startY: 0,
      endY: 0,
      confidence:0,
    });
    let imgSrc = ref("");
   

    function onFileChange(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;

      error.value = "";
      file.value = files[0];
      console.log(file.value)

      playSelectedFile(file)
   
    }
  
    var video = document.createElement("video")

    var canvas = document.querySelector("#prevImgCanvas");

    video.addEventListener('loadeddata', function() {
      reloadRandomFrame();
    }, false);

    video.addEventListener('seeked', function() {
      var context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, window.innerWidth, window.innerHeight);
    }, false);

    var playSelectedFile = function() {
      var fileURL = URL.createObjectURL(file.value);
      video.src = fileURL;
    }


    function reloadRandomFrame() {
      if (!isNaN(video.duration)) {
        var rand = Math.round(Math.random() * video.duration * 1000) + 1;
        video.currentTime = rand / 1000;
      }
    }

    console.log(video, canvas)

    async function onUploadFile() {
      if (!file.value) {
        error.value = "Please select a file!";

        return;
      }

      try {
        loading.value = true;
        advancedOptions.value.confidence /= 100 
        store.dispatch("FileProcessing/uploadVideo", {file:file.value, advancedOptions:advancedOptions.value});
        advancedOptions.value.confidence *= 100
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
      imgSrc,
    };
  },
};


</script>
