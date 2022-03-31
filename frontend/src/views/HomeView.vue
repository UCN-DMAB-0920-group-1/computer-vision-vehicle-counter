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
    
    const response = await fetch( process.env.VUE_APP_PROCESSING_ENDPOINT + "/auth?code=" + route.query["code"]
      , { method: "GET", } )

      const json = await response.json(); 

      if (json["jwt"].length > 0) {
        document.cookie = "jwt=" + json["jwt"];
        document.cookie = "loggedIn=" + "true";
    } 
  }
        store.dispatch("Authorization/checkLoggedin")
}
asyncfetch();


</script>
<style scoped>
#app{
  overflow: hidden;
}

</style>