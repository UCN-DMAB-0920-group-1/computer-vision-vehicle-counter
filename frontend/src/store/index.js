import { createStore } from "vuex";

import FileProcessing from "./module/FileProcessing";
import Detections from "./module/Detections";

export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    FileProcessing,
    Detections,
  },
});
