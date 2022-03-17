<template>
  <div>
    <img
      style="position: absolute; z-index: -99"
      id="image-frame"
      @load="onImageLoaded"
      src="img/highway.png"
      alt="Pølsemand"
    />
    <svg
      :height="imageSize.realHeight"
      :width="imageSize.realWidth"
      @click="onClick"
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
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  setup() {
    let imageSize = ref({});
    let drawPoints = ref([]);

    function onImageLoaded() {
      var myImg = document.querySelector("#image-frame");

      const width = myImg.naturalWidth;
      const height = myImg.naturalHeight;

      const realWidth = myImg.width;
      const realHeight = myImg.height;

      imageSize.value = {
        width: width,
        height: height,

        realWidth: realWidth,
        realHeight: realHeight,

        xScale: width / realWidth,
        yScale: height / realHeight,
      };
    }

    function onClick(e) {
      drawPoints.value.push({
        x: e.offsetX * imageSize.value.xScale,
        y: e.offsetY * imageSize.value.yScale,
        id: drawPoints.value.length,
      });
    }

    function deletePoint(id) {
      drawPoints.value = drawPoints.value.filter((point) => point.id != id);
    }

    return {
      drawPoints,
      imageSize,
      onImageLoaded,
      onClick,
      deletePoint,
    };
  },
};
</script>
