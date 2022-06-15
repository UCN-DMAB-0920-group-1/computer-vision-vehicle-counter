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
  // sends a GET request in order to download video data, from a specific task with _id_
  async getVideoData({ commit }, { id }) {
    const response = await fetch(process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection/" + id, {
      method: "GET",
      headers: { Authorization: getCookie("jwt") },
    });

    const json = await response.json();

    commit("setVideoData", json);
  },

  //Downloads all tasks from a specific user
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
