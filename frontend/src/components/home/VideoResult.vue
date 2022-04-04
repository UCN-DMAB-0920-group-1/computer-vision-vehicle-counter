<template>
  <div>
    <AlertBox v-for="video in finishedVideos" :key="video.id" :video="video"></AlertBox>

    <div>
      <section v-if="loading">
        <div class="flex justify-center items-center">
          <div class="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </section>
      <section>
        <div class="bg-violet-200 rounded-xl p-3">
          <div class=" bg-violet-300 rounded-lg p-3 shadow-md">
          <h1 class="font-bold text-lg">Video result ({{ videoIds.length }})</h1>
          <p class="text-left" v-for="entity in Object.entries(videoData)" :key="entity[0]"><span class="font-semibold ">{{ entity[0] }}:</span>: {{ entity[1] }}</p>
          </div>
          <!-- <p>Total vehicles: {{ totalCars }}</p> -->

          <button
            class="mx-auto px-3 shadow-xl block rounded-full bg-violet-700 p-2 text-white mt-4 transition ease-in-out hover:text-violet-700 hover:bg-white font-semibold"
            @click="downloadNewestData"
          >
            Download newest data
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import Pusher from "pusher-js";
import { ref, computed } from "vue";
import { useStore } from "vuex";
import AlertBox from "../core/AlertBox.vue";

export default {
  components: { AlertBox },
  setup() {
    const store = useStore();
    const vehicleTypes = ref([]);
    const loading = ref(false);
    const error = ref("");

    const videoIds = computed(() => store.getters["FileProcessing/videoIds"]);

    Pusher.logToConsole = false;
    const pusher = new Pusher(process.env.VUE_APP_PUSHER_KEY, { cluster: "eu" });
    var channel = pusher.subscribe("video-channel");
    channel.bind("video-event", function (data) {
      console.log(data);
      if (data.status == "Finished") {
        store.commit("Detections/addFinishedVideo", data);
        store.dispatch("Detections/getVideoData", {
          id: data.id,
        });
      }
    });
    async function downloadNewestData() {
      try {
        loading.value = true;
        await store.dispatch("Detections/getVideoData", {
          id: videoIds.value[videoIds.value.length - 1],
        });
      } catch (e) {
        error.value = e;
      } finally {
        loading.value = false;
      }
    }
    return {
      finishedVideos: computed(() => store.getters["Detections/finishedVideos"]),
      vehicleTypes,
      loading,
      downloadNewestData,
      videoData: computed(() => store.getters["Detections/videoData"]),
      totalCars: computed(() => {
        return vehicleTypes.value.reduce((total, item) => item.amount + total, 0);
      }),
      videoIds,
    };
  },
};
</script>
