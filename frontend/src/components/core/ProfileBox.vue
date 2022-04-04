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
import {getCookie} from "../../util/Cookie"
import jwt_decode from "jwt-decode";

let token = getCookie("jwt");
let json = jwt_decode(token);
let pictureSrc = ref(json["picture"]);
let name = ref(json["name"]);
</script>

<style lang="scss" scoped>

</style>