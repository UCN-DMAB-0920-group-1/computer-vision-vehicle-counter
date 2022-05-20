<template>
  <div class="">
    <NavBar></NavBar>
    <router-view></router-view>
    <div class="fixed bottom-6 z-10 flex flex-col justify-end flex-wrap max-h-full pt-6 gap-3 px-2">
      <AlertPopup v-for="item in alerts" :key="item" :text="item.event" :type="item.type"></AlertPopup>
    </div>
  </div>
</template>

<script setup>
import NavBar from "./components/core/NavBar.vue";
import { useStore } from "vuex";
import {computed} from "vue";
import AlertPopup from "@/components/core/AlertPopup.vue"
const store = useStore();

let alerts = computed(() => store.getters["AlertsList/list"]);
console.log(alerts.value)

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
