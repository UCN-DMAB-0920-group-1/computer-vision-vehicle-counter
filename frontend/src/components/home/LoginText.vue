<template>
  <div class="flex place-content-center text-grad text-4xl mt-40 gap-1 animate-bounce">
    <p>You should login</p>
  </div>
</template>

<style scoped>
p {
  background: -webkit-linear-gradient(
    rgb(255, 0, 0),
    rgb(229, 255, 0),
    rgb(0, 255, 13),
    rgb(25, 0, 255),
    rgb(247, 0, 255),
    rgb(255, 0, 85)
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  
}
 .bounce {
        animation-name: bounce;
        animation-timing-function: ease;
    }
    @keyframes bounce {
        0%   { transform: translateY(0); }
        50%  { transform: translateY(-100px); }
        100% { transform: translateY(0); }
    }

</style>
