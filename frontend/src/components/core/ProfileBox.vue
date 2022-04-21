<template>
    <div class="flex justify-start gap-2 p-1 text-white shadow-md bg-violet-700 sm:px-6 rounded-full
               hover:bg-white transition ease-in-out hover:text-violet-700">
            <p class="hidden my-auto sm:block font-semibold text-center shadow-sm">{{name}}</p>
        <div class="w-12 h-12 sm:-mr-5">
          <img class="rounded-full shadow-sm" :src="pictureSrc" alt="user image" />  
        </div>
    </div>     
</template>

<script setup>
import {ref} from "vue"
import {getPayloadValue} from "@/util/Cookie"
let pictureSrc = ref(getPayloadValue("picture"));
let name = ref(getPayloadValue("name"));
</script>
