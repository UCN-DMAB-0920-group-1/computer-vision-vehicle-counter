<template>
   <div class="sm:ml-6 right-12 w-12 h-12">
          <img class="rounded-full border border-gray-100 shadow-sm" :src="pictureSrc" alt="user image" />       
    </div>
</template>

<script setup>
import {ref} from "vue"
import {getCookie} from "../../util/Cookie"
import jwt_decode from "jwt-decode";

let token = getCookie("jwt");
let json = jwt_decode(token);
console.log(json["picture"]);
let pictureSrc = ref(json["picture"])
</script>

<style lang="scss" scoped>

</style>