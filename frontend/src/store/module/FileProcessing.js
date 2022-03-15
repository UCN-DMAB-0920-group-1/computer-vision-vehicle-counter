const state = {
  videoIds: [],
};

const mutations = {
  setVideoIds: (state, videoIds) => (state.videoIds = videoIds),
};
const actions = {
  async uploadVideo({ commit, state }, file) {
    const fd = new FormData();
    fd.append("file", file);

    const response = await fetch(
      process.env.VUE_APP_PROCESSING_ENDPOINT + "/video",
      {
        method: "POST",
        body: fd,
      }
    );

    const json = await response.json();
    state.videoIds.push(json.id); //Save ids for later use

    commit("setVideoIds", state.videoIds);
    console.log("RESPONSE: " + response.status, json);
  },
};
const getters = {
  videoIds: (state) => state.videoIds,
};

export default {
  state,
  namespaced: true,
  mutations,
  actions,
  getters,
};
