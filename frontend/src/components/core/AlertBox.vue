<template>
  <div
    class="bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3 shadow-md"
    role="alert"
    @click="onClick"
  >
    <div class="flex">
      <div>
        <p class="font-bold">Your video IST FINITO!</p>
        <p class="text-sm">We found {{ video.detections.car }} cars in total, in video {{ video.id }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex";

export default {
  props: {
    video: Object,
  },
  setup(props) {
    const store = useStore();

    function onClick() {
      console.log("clicked on video with id:", props.video.id);
      store.commit("Detections/removeFinishedVideoNotification", props.video.id);
    }

    return {
      onClick,
    };
  },
};
</script>
