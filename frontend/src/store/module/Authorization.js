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
  