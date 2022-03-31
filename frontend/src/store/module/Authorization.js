import { isLoggedIn} from "./getCookie";

const state = {
    Login: false,
    Jwt: "",
};

const mutations = {
    setLoginData: (state, Login) => (state.Login = Login),
    setJwtData: (state, jwt) => (state.Jwt = jwt),
};
const actions = {
    login() {
    },
    logout({ commit }) {
        commit("setLoginData", false);
    },
    checkLoggedin({commit}){
        const loggedIn = isLoggedIn();
        commit("setLoginData", loggedIn);
    },
};
const getters = {
    Login: (state) => state.Login,
    Jwt: (state) => state.Jwt,
};

export default {
    state,
    namespaced: true,
    mutations,
    actions,
    getters,
};