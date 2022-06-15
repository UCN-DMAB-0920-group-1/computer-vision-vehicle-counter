const state = {
  Alerts: [],
};

const mutations = {
  addAlert: (state, { e, type }) => state.Alerts.push({ event: e, type: type }),
  removeAlert: (state) => state.Alerts.pop(),
};

const actions = {
  // Adds an alert and removes it after timeout is over
  addAlert({ commit }, { e, type }) {
    commit("addAlert", { e, type });
    setTimeout(() => {
      commit("removeAlert");
    }, 7000);
  },
};

const getters = {
  list: (state) => state.Alerts,
};

export default {
  state,
  namespaced: true,
  mutations,
  actions,
  getters,
};
