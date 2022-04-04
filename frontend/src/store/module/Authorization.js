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
    async login({ dispatch},{routeCode}) {
        const response = await fetch( process.env.VUE_APP_PROCESSING_ENDPOINT + "/auth?code=" + routeCode
      , { method: "GET", } )

      const json = await response.json(); 

      if (json["jwt"].length > 0) {
        document.cookie = "jwt=" + json["jwt"];
        document.cookie = "loggedIn=" + "true";
        }
    
        dispatch("checkLoggedin")
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