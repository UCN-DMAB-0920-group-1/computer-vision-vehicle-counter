<template>
  <div v-if="loggedin">
    <div
      class="grid grid-cols-1 gap-3 sm:grid-cols-1 max-w-7xl mx-auto"
    >
      <div class="bg-violet-200 rounded-xl shadow-xl ">
        <FileUpload></FileUpload>
      
      </div>
          <VideoResult></VideoResult>
    </div>

  </div>
</template>

<script setup>
import FileUpload from "@/components/home/FileUpload.vue";
import VideoResult from "@/components/home/VideoResult.vue";
import { useRoute } from 'vue-router'
import { useStore } from "vuex";
import {computed} from "vue";
const route = useRoute()
const store = useStore()
let loggedin = computed(() => store.getters["Authorization/Login"]);


const asyncDispatch = async () =>  {
  await store.dispatch("Authorization/saveGoogleCode", route.query["code"])
}
asyncDispatch()
</script>
