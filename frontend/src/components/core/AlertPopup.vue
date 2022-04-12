<template>
  <div v-if="alertOpen" :class="typeClasses" class="box text-white px-3 py-2 border-0 rounded relative transition ease-in-out delay-500">
    <span class="text-xl inline-block mr-5 align-middle">
      <i class="fas fa-bell"></i>
    </span>
    <span class="inline-block align-middle mr-8">
      <b class="capitalize">{{headerText}}:</b> {{props.text}}
    </span>
    <button class="absolute bg-transparent text-2xl my-2 font-semibold leading-none right-0 top-0 mr-6 outline-none focus:outline-none" @click="closeAlert()">
      <span>×</span>
    </button>
  </div>
</template>

<script setup>
import {ref, defineProps,onMounted } from "vue"

let typeClasses = ""
let headerText = ""
switch(props.type) {
  case "Error":
    headerText = props.type
    typeClasses = "bg-red-500"
    break;
  case "Success":
    headerText = props.type
    typeClasses = "bg-green-500"
    break;
  case "Warning":
    headerText = props.type
    typeClasses = "bg-yellow-500"
    break;
  default:
    headerText = "Error"
    typeClasses = "bg-red-500"
}
const props = defineProps(["text","type"])
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