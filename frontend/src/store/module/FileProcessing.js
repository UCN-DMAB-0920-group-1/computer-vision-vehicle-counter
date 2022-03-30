const state = {

    videoIds: [],
    videoUrl: "",
    videoBBox: [],
    advancedOptions: {
        enabled: true,
        drawBoundingBox: true,
        confidence: 70,
        maxDistanceBetweenPoints: 20,
    },
    bboxCoordinates: {
        startX: 0,
        endX: 1920,
        startY: 0,
        endY: 1080,
    },
};

const mutations = {
    setVideoIds: (state, videoIds) => (state.videoIds = videoIds),
    setVideoUrl: (state, url) => (state.videoUrl = url),
    setVideoBbox: (state, videoBBox) => (state.videoBBox = videoBBox),
    saveOptions: (state, options) => (state.advancedOptions = options),
    saveBboxCoordinates: (state, coordinates) =>
        (state.bboxCoordinates = coordinates),
};
const actions = {
    async uploadVideo({ commit, state }, { file, jwt }) {
        console.log(jwt)
        const formData = new FormData();
        formData.append("file", file);
        formData.append("jwt", jwt);

        state.advancedOptions["confidence"] /= 100;
        Object.entries(state.advancedOptions).forEach(([key, value]) => {
            formData.append(key, value);
            console.log(key, value);
        });
        state.advancedOptions["confidence"] *= 100;

        let bbox = [];
        //Check if draw is true and if there are more than 2 points drawn else make default box 
        if (state.advancedOptions.drawBoundingBox && state.videoBBox.length > 2) {
            bbox = state.videoBBox.map(function(point) {
                return [parseInt(point.scaledX), parseInt(point.scaledY)];
            });
        } else {
            bbox = [
                [state.bboxCoordinates.startX, state.bboxCoordinates.startY],
                [state.bboxCoordinates.endX, state.bboxCoordinates.startY],
                [state.bboxCoordinates.endX, state.bboxCoordinates.endY],
                [state.bboxCoordinates.startX, state.bboxCoordinates.endY],
            ];
        }

        formData.append("bbox", JSON.stringify(bbox));

        const response = await fetch(
            process.env.VUE_APP_PROCESSING_ENDPOINT + "/detection", {
                method: "POST",
                body: formData,
            }
        );

        const json = await response.json();
        state.videoIds.push(json.id); //Save ids for later use


        commit("setVideoIds", state.videoIds);
        return json.id;
    },
    saveVideoUrl({ commit }, url) {
        console.log("VIDEO URL:", url);
        commit("setVideoUrl", url);
    },

};
const getters = {
    videoIds: (state) => state.videoIds,
    videoUrl: (state) => state.videoUrl,
    advancedOptions: (state) => state.advancedOptions,
    bboxCoordinates: (state) => state.bboxCoordinates,
};

export default {
    state,
    namespaced: true,
    mutations,
    actions,
    getters,
};