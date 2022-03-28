const state = {
  videoData: [],
  finishedVideos: [],
};

const mutations = {
  setVideoData: (state, videoData) => (state.videoData = videoData),
  addFinishedVideo: (state, data) => state.finishedVideos.push(data),
  removeFinishedVideoNotification: (state, id) =>
    (state.finishedVideos = state.finishedVideos.filter((item) => item.id != id)),
};
const actions = {
  async getVideoData({ commit }, { id }) {
    const response = await fetch(process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection/" + id, {
      method: "GET",
    });

    const json = await response.json();

    commit("setVideoData", json);
  },
  async downloadVideo({ commit }, file) {
    const fd = new FormData();
    fd.append("file", file);

    const response = await fetch(process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection", {
      method: "POST",
      body: fd,
    });

    const json = await response.json();
    state.videoIds.push(json.id); //Save ids for later use

    commit("setVideoIds", state.videoIds);
  },
};
const getters = {
  videoData: (state) => state.videoData,
  finishedVideos: (state) => state.finishedVideos,
};

export default {
  state,
  namespaced: true,
  mutations,
  actions,
  getters,
};
