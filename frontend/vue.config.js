const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  devServer: {
        proxy: process.env.VUE_APP_PROCESSING_ENDPOINT,
    },
  transpileDependencies: true
})
