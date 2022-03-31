import { isLoggedIn, logoutCookie} from "@/util/Cookie";

const state = {
    login: false,
    jwt: "",
};

const mutations = {
    setLoginData: (state, login) => (state.login = login),
    setJwtData: (state, jwt) => (state.jwt = jwt),
};
const actions = {
    login() {
    },
    logout({dispatch}) {
        logoutCookie();
        dispatch("checkLoggedin");
    },
    checkLoggedin({ commit }) {
        const loggedIn = isLoggedIn();
        commit("setLoginData", loggedIn);
    },
};
const getters = {
    loginState: (state) => state.login,
    jwt: (state) => state.jwt,
};

export default {
    state,
    namespaced: true,
    mutations,
    actions,
    getters,
};