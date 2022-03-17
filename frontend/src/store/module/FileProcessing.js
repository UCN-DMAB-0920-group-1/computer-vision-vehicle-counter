const state = {
  videoIds: [],
  videoUrl: "",
  videoBBox: [],
};

const mutations = {
  setVideoIds: (state, videoIds) => (state.videoIds = videoIds),
  setVideoUrl: (state, url) => (state.videoUrl = url),
  setVideoBbox: (state, videoBBox) => (state.videoBBox = videoBBox),
};
const actions = {
  async uploadVideo({ commit, state }, { file, advancedOptions }) {
    const formData = new FormData();
    formData.append("file", file);

    Object.entries(advancedOptions).forEach(([key, value]) => {
      formData.append(key, value);
      console.log(key, value);
    });

    const bbox = state.videoBBox.map(function (point) {
      return [parseInt(point.scaledX), parseInt(point.scaledY)];
    });

    formData.append("bbox", JSON.stringify(bbox));

    const response = await fetch(
      process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection",
      {
        method: "POST",
        body: formData,
      }
    );

    const json = await response.json();
    state.videoIds.push(json.id); //Save ids for later use

    commit("setVideoIds", state.videoIds);
  },
  saveVideoUrl({ commit }, url) {
    console.log("VIDEO URL:", url);
    commit("setVideoUrl", url);
  },
};
const getters = {
  videoIds: (state) => state.videoIds,
  videoUrl: (state) => state.videoUrl,
};

export default {
  state,
  namespaced: true,
  mutations,
  actions,
  getters,
};
