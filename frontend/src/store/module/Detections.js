import { getCookie, getPayloadValue } from "@/util/Cookie";

const state = {
  videoData: [],
  finishedVideos: [],
  userVideos: [],
};

const mutations = {
  setUserVideos: (state, userVideos) => (state.userVideos = userVideos),
  setVideoData: (state, videoData) => (state.videoData = videoData),
  addFinishedVideo: (state, data) => state.finishedVideos.push(data),
  removeFinishedVideoNotification: (state, id) =>
    (state.finishedVideos = state.finishedVideos.filter((item) => item.id != id)),
};
const actions = {
  async getVideoData({ commit }, { id }) {
    const response = await fetch(process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection/" + id, {
      method: "GET",
      headers: { Authorization: getCookie("jwt") },
    });

    const json = await response.json();

    commit("setVideoData", json);
  },
  async downloadVideo({ commit }, file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection", {
      method: "POST",
      body: formData,
      headers: { Authorization: getCookie("jwt") },
    });

    const json = await response.json();
    state.videoIds.push(json.id); //Save ids for later use

    commit("setVideoIds", state.videoIds);
  },
  async downloadUserDetections({ commit }) {
    const UUID = getPayloadValue("UUID");
    const response = await fetch(process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection/user?UUID=" + UUID, {
      method: "GET",
      headers: { Authorization: getCookie("jwt") },
    });
    const json = await response.json();

    commit("setUserVideos", json.reverse());
  },
};
const getters = {
  videoData: (state) => state.videoData,
  finishedVideos: (state) => state.finishedVideos,
  userVideos: (state) => state.userVideos,
};

export default {
  state,
  namespaced: true,
  mutations,
  actions,
  getters,
};
