const state = {
    videoData: [],
};

const mutations = {
    setVideoData: (state, videoData) => (state.videoData = videoData),
};
const actions = {
    async getVideoData({ commit }, { id, jwt }) {
        console.log(jwt)
        const response = await fetch(
            process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection/" + id, {
                method: "GET",
                headers: { "Authorization": jwt },
            }
        );

        const json = await response.json();

        commit("setVideoData", json);
    },
    async downloadVideo({ commit }, file) {
        const fd = new FormData();
        fd.append("file", file);

        const response = await fetch(
            process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection", {
                method: "POST",
                body: fd,
            }
        );

        const json = await response.json();
        state.videoIds.push(json.id); //Save ids for later use

        commit("setVideoIds", state.videoIds);
    },
};
const getters = {
    videoData: (state) => state.videoData,
};

export default {
    state,
    namespaced: true,
    mutations,
    actions,
    getters,
};