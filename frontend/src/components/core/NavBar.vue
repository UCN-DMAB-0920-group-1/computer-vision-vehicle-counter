<template>
  <div class="flex justify-evenly sm:justify-center m-2 mb-2 mx-auto bg-violet-500 -my-2 py-4">
    <div>
    <router-link
      to="/"
      class="shadow-xl block rounded-full bg-violet-700 p-4 px-8 text-white mx-2 transition ease-in-out hover:text-violet-700 hover:bg-white font-semibold"
    >
      Home</router-link
    >
    </div>
    <div class="hidden  sm:block">

    <router-link
      to="/about"
      class="shadow-xl block rounded-full bg-violet-700 px-8 text-white p-4 mx-2 ease-in-out hover:text-violet-700 hover:bg-white font-semibold"
    >
      About</router-link
    >
    </div>
      <div v-if="loggedin">  
    <button
      @click="logout"
      to="/logout"
      
      class="shadow-xl block rounded-full bg-violet-700 p-4 px-8 text-white mx-2 transition ease-in-out hover:text-violet-700 hover:bg-white font-semibold"
    >
      Logout
    </button>
      </div>

    <div v-else>
      <div>

     <router-link
      to="/login"
      
      class="shadow-xl block rounded-full bg-violet-700 p-4 px-8 text-white mx-2 transition ease-in-out hover:text-violet-700 hover:bg-white font-semibold"
    >
      Login
    </router-link>
      </div>
      
    
</div>
    <div v-if="loggedin">
    <ProfileBox></ProfileBox>
    </div>
    
  </div>
</template>

<script setup>
import {useStore} from "vuex"
import {computed} from "vue"
import ProfileBox from "@/components/core/ProfileBox.vue"
const store = useStore()
let loggedin = computed(() => store.getters["Authorization/loginState"])


function logout(){
  store.dispatch("Authorization/logout")
}


</script>

<style scoped></style>
