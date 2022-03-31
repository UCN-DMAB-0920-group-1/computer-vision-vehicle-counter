<template>
  <div class="">
    <NavBar></NavBar>
    <router-view></router-view>
        
    <AlertBox v-for="video in finishedVideos" :key="video.id" :video="video"></AlertBox>
  </div>
</template>

<script>

import NavBar from "./components/core/NavBar.vue";
import AlertBox from "./components/core/AlertBox.vue";
export default {
  components: { NavBar, AlertBox },
  setup() {


  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
