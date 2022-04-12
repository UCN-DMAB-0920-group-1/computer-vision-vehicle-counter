import { createStore } from "vuex";

import FileProcessing from "./module/FileProcessing";
import Detections from "./module/Detections";
import Authorization from "./module/Authorization";
import AlertsList from "./module/AlertsList";

export default createStore({
    state: {},
    getters: {},
    mutations: {},
    actions: {},
    modules: {
        FileProcessing,
        Detections,
        Authorization,
        AlertsList,
    },
});