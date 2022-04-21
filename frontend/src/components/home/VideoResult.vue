<template>
  <div>    
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
          <div class="bg-violet-300 rounded-lg p-3 shadow-md">
            <h1 class="font-bold text-lg">Video result ({{ videoIds.length }})</h1>
            <DetectionResults :video="videoData"></DetectionResults>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import DetectionResults from "@/components/core/detectionResults.vue";
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { getPayloadValue } from "@/util/Cookie";

export default {
  components: { DetectionResults },
  setup() {
    const store = useStore();
    const vehicleTypes = ref([]);
    const loading = ref(false);
    const error = ref("");

    const videoIds = computed(() => store.getters["FileProcessing/videoIds"]);
    const pusher = computed(() => store.getters["Authorization/pusherSession"]);

    if (pusher.value != null) {
      const uuid = getPayloadValue("UUID");

      var channel = pusher.value.subscribe(`private-video-channel-${uuid}`);
      channel.bind(`video-event`, function (data) {
        if (data.status == "Finished") {
          store.commit("Detections/addFinishedVideo", data);
          store.dispatch("AlertsList/addAlert", {e:"Your video is finished!", type:"Success"});
          store.dispatch("Detections/getVideoData", {
            id: data.id,
          });
        }
      });
    }

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
