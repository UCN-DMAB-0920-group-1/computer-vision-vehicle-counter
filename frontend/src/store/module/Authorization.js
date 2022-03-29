const state = {
    Login: false,
    Jwt: "",
    GoogleToken: ""
};

const mutations = {
    setJwtData: (state, Jwt) => (state.Jwt = Jwt),
    setGoogleTokenData: (state, GoogleToken) => (state.GoogleToken = GoogleToken),
    setLoginData: (state, Login) => (state.Login = Login),
};
const actions = {
    async saveGoogleCode({ commit }, code) {
        console.log("from store code:", code);

        const response = await fetch(
            process.env.VUE_APP_PROCESSING_ENDPOINT + "auth?code=" + code, {
                method: "GET",
            }
        )
        const json = await response.json()
        console.log(json)
        commit("setJwtData", json["jwt"]);
        commit("setLoginData", true)
    },
    logout({ commit }) {
        commit("setJwtData", "")
        commit("setLoginData", false)
    },
};
const getters = {
    Login: (state) => state.Login,
    Jwt: (state) => state.Jwt,
    Google: (state) => state.GoogleToken,
};

export default {
    state,
    namespaced: true,
    mutations,
    actions,
    getters,
};