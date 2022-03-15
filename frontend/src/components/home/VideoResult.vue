<template>
  <div class="bg-blue-200 rounded-xl p-3">
    <h1>Video result</h1>
    <p v-for="vehicle in vehicleTypes" :key="vehicle.type">
      {{ vehicle.type }}: {{ vehicle.amount }}
    </p>
    <p>Total vehicles: {{ totalCars }}</p>

    <button class="block w-full rounded-full bg-blue-300 p-2 text-white mt-4">
      Download visualized file
    </button>
  </div>
</template>

<script>
import { ref, computed } from "vue";

export default {
  setup() {
    const vehicleTypes = ref([
      {
        type: "car",
        amount: 10,
      },
      {
        type: "truck",
        amount: 23,
      },
      {
        type: "bus",
        amount: 2,
      },
    ]);

    const totalCars = computed(() => {
      return vehicleTypes.value.reduce((total, item) => item.amount + total, 0);
    });

    return {
      vehicleTypes,
      totalCars,
    };
  },
};
</script>
