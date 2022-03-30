<template>
<div class="grid grid-cols-1 gap-3 sm:grid-cols-1 max-w-7xl mx-auto">
  <div class=" flex justify-center rounded-xl shadow-md overflow-hidden bg-green-100 m-2 border-solid	border-2	border-green-400" role="alert" @click="onClick">
    <div class="">
      <div class="p-4">
        <div class="uppercase tracking-wide text-md text-indigo-500 font-semibold text-center text-black		">Your video is done </div>
        <p class="block mt-1 text-lg leading-tight font-medium text-black hover:underline text-center	">Video: {{ video.id }} </p>
        <p class="mt-2 text-gray-500 text-center">We found {{ video.detections.car }} cars in total.</p>
      </div>
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
