<template>
  <div>
    <section v-if="loading">
      <div class="flex justify-center items-center">
        <div
          class="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full"
          role="status"
        >
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </section>
    <section>
      <div class="bg-blue-200 rounded-xl p-3">
        <h1 class="font-bold text-lg">Video result ({{ videoIds.length }})</h1>
        <p v-for="entity in Object.entries(videoData)" :key="entity[0]">
          {{ entity[0] }}: {{ entity[1] }}
        </p>
        <!-- <p>Total vehicles: {{ totalCars }}</p> -->

        <button
          class="block w-full rounded-full bg-blue-300 p-2 text-white mt-4"
          @click="downloadNewestData"
        >
          Download newest data
        </button>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();

    const vehicleTypes = ref([]);
    const loading = ref(false);
    const error = ref("");

    const videoIds = computed(() => store.getters["FileProcessing/videoIds"]);

    async function downloadNewestData() {
      try {
        loading.value = true;
        store.dispatch("Detections/getVideoData", {
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
        return vehicleTypes.value.reduce(
          (total, item) => item.amount + total,
          0
        );
      }),
      videoIds,
    };
  },
};
</script>
