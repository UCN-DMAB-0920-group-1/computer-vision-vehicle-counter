<template>
    <div class="flex gap-4 mt-2">
        <div class="sm:ml-6 right-12 w-12 h-12">
          <img class="rounded-full border border-violet-700 shadow-sm" :src="pictureSrc" alt="user image" />  
        </div>
            <p class="hidden my-auto sm:block text-white font-semibold text-center shadow-sm">{{name}}</p>
    </div>     
</template>

<script setup>
import {ref} from "vue"
import {getPayloadValue} from "../../util/Cookie"
let pictureSrc = ref(getPayloadValue("picture"));
let name = ref(getPayloadValue("name"));
</script>

<style lang="scss" scoped>

</style>