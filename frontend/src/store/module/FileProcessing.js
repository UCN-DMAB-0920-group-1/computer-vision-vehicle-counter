import { getCookie } from "@/util/Cookie";

const state = {
  videoIds: [],
  videoUrl: "",
  videoDrawPoints: [],
  advancedOptions: {
    enabled: true,
    drawBoundingBox: true,
    confidence: 70,
    maxDistanceBetweenPoints: 20,
  },
  bboxCoordinates: {
    startX: 0,
    endX: 100,
    startY: 0,
    endY: 100,
  },
  blobLink: ""
};

const mutations = {
  setVideoIds: (state, videoIds) => (state.videoIds = videoIds),
  setVideoUrl: (state, url) => (state.videoUrl = url),
  setvideoDrawPoints: (state, videoDrawPoints) => (state.videoDrawPoints = videoDrawPoints),
  addPointToPolygon: (state, point) => state.videoDrawPoints.push(point),
  removePointfromPolygon: (state, id) =>
    (state.videoDrawPoints = state.videoDrawPoints.filter((item) => item.id != id)),
  saveOptions: (state, options) => (state.advancedOptions = options),
  saveBboxCoordinates: (state, coordinates) => (state.bboxCoordinates = coordinates),
  setBlobLink: (state, link) => (state.blobLink = link),
};
const actions = {
  async uploadVideo({ commit, state }, { file }) {
    const formData = new FormData();
    formData.append("file", file);

    state.advancedOptions["confidence"] /= 100;
    Object.entries(state.advancedOptions).forEach(([key, value]) => {
      formData.append(key, value);
      console.log(key, value);
    });
    state.advancedOptions["confidence"] *= 100;

    let bbox = [];
    //Check if draw is true and if there are more than 2 points drawn else make default box
    if (state.advancedOptions.drawBoundingBox && state.videoDrawPoints.length > 2) {
      bbox = state.videoDrawPoints.map(function (point) {
        return [parseInt(point.scaledX), parseInt(point.scaledY)];
      });
    } else {
      bbox = {};
    }

    formData.append("bbox", JSON.stringify(bbox));

    const response = await fetch(process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection", {
      method: "POST",
      body: formData,
      headers: { Authorization: getCookie("jwt") },
    });

    const json = await response.json();
    state.videoIds.push(json.id); //Save ids for later use

    commit("setVideoIds", state.videoIds);
    return json.id;
  },
  saveVideoUrl({ commit }, url) {
    console.log("VIDEO URL:", url);
    commit("setVideoUrl", url);
  },
  async downloadVideo({ commit, dispatch }, id) {
    const url =process.env.VUE_APP_PROCESSING_ENDPOINT + "detection/" + id + "/video";

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers:{ Authorization: getCookie('jwt')},
      })
      if (response.ok) {
        const blob = await response.blob();
        const blobLink = window.URL.createObjectURL(blob);
        commit("setBlobLink", blobLink);
        return blobLink
      } else {
        throw "could not fetch";  
      }
    } catch  {
      dispatch("AlertsList/addAlert", {e:"Could not download file", type:"Error"}, {root:true})
    }
  },
};
const getters = {
  videoIds: (state) => state.videoIds,
  videoUrl: (state) => state.videoUrl,
  advancedOptions: (state) => state.advancedOptions,
  bboxCoordinates: (state) => state.bboxCoordinates,
  videoDrawPoints: (state) => state.videoDrawPoints,
  getBlobLink: (state) => state.blobLink,
};

export default {
  state,
  namespaced: true,
  mutations,
  actions,
  getters,
};
