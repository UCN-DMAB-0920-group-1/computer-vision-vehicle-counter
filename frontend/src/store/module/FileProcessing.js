const state = {
    videoIds: [],
};

const mutations = {
    setVideoIds: (state, videoIds) => (state.videoIds = videoIds),
};
const actions = {
    async uploadVideo({ commit, state }, { file, advancedOptions }) {
        const fd = new FormData();
        fd.append("file", file);
        Object.entries(advancedOptions).forEach(([key, value]) => {
            fd.append(key, value)
            console.log(key, value)
        })

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
    videoIds: (state) => state.videoIds,
};

export default {
    state,
    namespaced: true,
    mutations,
    actions,
    getters,
};