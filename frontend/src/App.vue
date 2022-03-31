<template>
  <div class="">
    <NavBar></NavBar>
    <router-view></router-view>

    <AlertBox v-for="video in finishedVideos" :key="video.id" :video="video"></AlertBox>
  </div>
</template>

<script setup>
import AlertBox from "./components/core/AlertBox.vue";
import NavBar from "./components/core/NavBar.vue";
import Pusher from "pusher-js";
import { useStore } from "vuex";
import { computed } from "vue";

const store = useStore();

store.dispatch("Authorization/checkLoggedin");

let finishedVideos = computed(() => store.getters["Detections/finishedVideos"]);

Pusher.logToConsole = false;
const pusher = new Pusher(process.env.VUE_APP_PUSHER_KEY, { cluster: "eu" });
const channel = pusher.subscribe("video-channel");
channel.bind("video-event", function (data) {
  console.log(data);
  if (data.status == "Finished") {
    store.commit("Detections/addFinishedVideo", data);
    store.dispatch("Detections/getVideoData", { id: data.id });
  }
});
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
