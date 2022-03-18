<template>
  <div oncontextmenu="return false;">
    <input
      type="range"
      name="range"
      @change="changeTime"
      v-model="timestampValue"
      :max="duration"
      class="w-full h-1 shadow-xl bg-blue-100 appearance-none rounded-lg"
    />
    <video
      style="position: absolute; z-index: -99"
      id="video-frame"
      @loadeddata="onImageLoaded"
      :src="videoUrl"
      alt="Video source"
    />
    <svg
      :height="imageSize.height"
      :width="imageSize.width"
      @click="onClick"
      v-if="options.drawBoundingBox"
    >
      <line
        v-for="(point, i) in drawPoints"
        :key="i"
        :x1="point.x"
        :y1="point.y"
        :x2="drawPoints[(i + 1) % drawPoints.length].x"
        :y2="drawPoints[(i + 1) % drawPoints.length].y"
        style="stroke: rgb(255, 0, 0); stroke-width: 2"
      />
      <circle
        v-for="point in drawPoints"
        :key="point.id"
        @click.right="deletePoint(point.id)"
        :cx="point.x"
        :cy="point.y"
        r="10"
        stroke="black"
        stroke-width="1"
        fill="red"
      />
    </svg>
    <svg v-else :height="imageSize.height" :width="imageSize.width">
      <line
        :x1="bboxCoordinates.startX"
        :y1="bboxCoordinates.startY"
        :x2="bboxCoordinates.endX"
        :y2="bboxCoordinates.startY"
        style="stroke: rgb(255, 0, 0); stroke-width: 2"
      />
      <line
        :x1="bboxCoordinates.endX"
        :y1="bboxCoordinates.startY"
        :x2="bboxCoordinates.endX"
        :y2="bboxCoordinates.endY"
        style="stroke: rgb(255, 0, 0); stroke-width: 2"
      />
      <line
        :x1="bboxCoordinates.endX"
        :y1="bboxCoordinates.endY"
        :x2="bboxCoordinates.startX"
        :y2="bboxCoordinates.endY"
        style="stroke: rgb(255, 0, 0); stroke-width: 2"
      />
      <line
        :x1="bboxCoordinates.startX"
        :y1="bboxCoordinates.endY"
        :x2="bboxCoordinates.startX"
        :y2="bboxCoordinates.startY"
        style="stroke: rgb(255, 0, 0); stroke-width: 2"
      />
    </svg>
  </div>
</template>

<script>
import { ref, computed, watch } from "vue";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();

    let imageSize = ref({});
    let drawPoints = ref([]);

    let duration = ref(0);
    let timestampValue = ref(0);

    function onImageLoaded() {
      const video = document.getElementById("video-frame");
      duration.value = video.duration;

      const width = video.offsetWidth;
      const height = video.offsetHeight;

      const videoWidth = video.videoWidth;
      const videoHeight = video.videoHeight;

      imageSize.value = {
        width: width,
        height: height,

        videoWidth: videoWidth,
        videoHeight: videoHeight,

        scaleX: videoWidth / width,
        scaleY: videoHeight / height,
      };
    }

    function onClick(e) {
      drawPoints.value.push({
        //X and Y relative to screen size
        x: e.offsetX,
        y: e.offsetY,

        // X and Y relative to video size
        scaledX: e.offsetX * imageSize.value.scaleX,
        scaledY: e.offsetY * imageSize.value.scaleY,
        id: drawPoints.value.length,
      });
    }

    function deletePoint(id) {
      drawPoints.value = drawPoints.value.filter((point) => point.id != id);
    }

    function changeTime() {
      const video = document.getElementById("video-frame");
      video.currentTime = timestampValue.value;
    }

    watch(drawPoints.value, (currentValue) => {
      store.commit("FileProcessing/setVideoBbox", currentValue);
    });

    return {
      drawPoints,
      imageSize,
      videoUrl: computed(() => store.getters["FileProcessing/videoUrl"]),
      options: computed(() => store.getters["FileProcessing/advancedOptions"]),
      bboxCoordinates: computed(
        () => store.getters["FileProcessing/bboxCoordinates"]
      ),
      duration,
      timestampValue,
      changeTime,
      onImageLoaded,
      onClick,
      deletePoint,
    };
  },
};
</script>
