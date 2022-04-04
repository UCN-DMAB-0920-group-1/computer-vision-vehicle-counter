<template>
  <div>
    <div
      v-if="loggedIn"
      class="grid grid-cols-1 gap-3 sm:grid-cols-1 max-w-7xl mx-auto duration-300"
    >
      <div class="bg-violet-200 rounded-xl shadow-xl ">
        <FileUpload></FileUpload>
      
      </div>
          <VideoResult></VideoResult>
    </div>
      <div v-else>
        <LoginText></LoginText>
      </div>
  </div>
 
</template>

<script setup>
import FileUpload from "@/components/home/FileUpload.vue";
import VideoResult from "@/components/home/VideoResult.vue";
import LoginText from "@/components/home/LoginText.vue";
import {useRoute} from 'vue-router'
import {useStore} from "vuex"
import {computed} from "vue"
const route = useRoute()
const store = useStore()


let loggedIn = computed(() => store.getters["Authorization/loginState"])



const asyncfetch = async () =>  {
  if(!loggedIn.value){
   const routeCode = route.query["code"]
   store.dispatch("Authorization/login",{routeCode}) 
    
  }
}
asyncfetch();


</script>
<style scoped>
#app{
  overflow: hidden;
}

</style>