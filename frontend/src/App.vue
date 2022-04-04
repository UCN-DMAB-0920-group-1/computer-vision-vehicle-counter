<template>
  <div class="">
    <NavBar></NavBar>
    <router-view></router-view>
  </div>
</template>

<script setup>
import NavBar from "./components/core/NavBar.vue";
import { useStore } from "vuex";

const store = useStore();

store.dispatch("Authorization/checkLoggedin");
store.dispatch("Authorization/authenticatePusher");
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
