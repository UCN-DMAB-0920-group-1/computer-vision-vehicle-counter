<template>
  <div v-if="alertOpen" class="box text-white px-6 py-4 border-0 rounded relative mb-4 bg-red-500 transition ease-in-out delay-500">
    <span class="text-xl inline-block mr-5 align-middle">
      <i class="fas fa-bell"></i>
    </span>
    <span class="inline-block align-middle mr-8">
      <b class="capitalize">error!</b> {{props.error}}
    </span>
    <button class="absolute bg-transparent text-2xl font-semibold leading-none right-0 top-0 mt-4 mr-6 outline-none focus:outline-none" @click="closeAlert()">
      <span>×</span>
    </button>
  </div>
</template>

<script setup>
import {ref, defineProps,onMounted } from "vue"

const props = defineProps(["error"])
let alertOpen = ref(true)

    function closeAlert(){
        alertOpen.value = false;
    }

onMounted(() => {
  setTimeout(() => {
    closeAlert();
  }, 3000);
});
</script>

<style scoped>
.box{
  opacity: 1;
  animation: fade 1.5s ease-in-out;
}
@keyframes fade{
  0% {opacity: 0;}
  100% {opacity: 1;}
}
</style>