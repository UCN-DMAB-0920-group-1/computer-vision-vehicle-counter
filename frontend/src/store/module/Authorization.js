import { isLoggedIn, logoutCookie, getCookie } from "@/util/Cookie";
import Pusher from "pusher-js";

const state = {
  loggedIn: false,
  jwt: "",
  pusherSession: null,
};

const mutations = {
  setLoginData: (state, login) => (state.loggedIn = login),
  setJwtData: (state, jwt) => (state.jwt = jwt),
  setPusherSession: (state, pusher) => (state.pusherSession = pusher),
};
const actions = {
  login({ dispatch, state }, { route }) {
    console.log(route);

    if (state.loggedIn) {
      dispatch("authenticatePusher");
    }
  },
  logout({ dispatch }) {
    logoutCookie();
    dispatch("checkLoggedin");
  },
  checkLoggedin({ commit }) {
    const loggedIn = isLoggedIn();
    commit("setLoginData", loggedIn);
  },
  authenticatePusher({ commit }) {
    Pusher.logToConsole = false;

    const authUrl = `${process.env.VUE_APP_PROCESSING_ENDPOINT}/auth/pusher`;
    let authorizer = (channel, options) => {
      console.log("PUSHER authorizer", options);
      return {
        authorize: (socketId, callback) => {
          console.log("PUSHER AUTH!", socketId);
          const body = JSON.stringify({
            socket_id: socketId,
            channel_name: channel.name,
          });

          console.log("BODY:", body);
          const jwt = getCookie("jwt");
          fetch(authUrl, {
            method: "POST",
            headers: new Headers({ "Content-Type": "application/json", Authorization: `Bearer: ${jwt}` }),
            body: body,
          })
            .then((res) => {
              if (!res.ok) {
                throw new Error(`Received ${res.statusCode} from ${authUrl}`);
              }

              return res.json();
            })
            .then((data) => {
              console.log("AYO IT WORKED!", data);
              callback(null, data);
            })
            .catch((err) => {
              callback(new Error(`Error calling auth endpoint: ${err}`), {
                auth: "",
              });
            });
        },
      };
    };

    const pusher = new Pusher(process.env.VUE_APP_PUSHER_KEY, {
      cluster: "eu",
      authEndpoint: authUrl,
      authorizer: authorizer,
    });

    commit("setPusherSession", pusher);
  },
};
const getters = {
  loginState: (state) => state.loggedIn,
  jwt: (state) => state.jwt,
  pusherSession: (state) => state.pusherSession,
};

export default {
  state,
  namespaced: true,
  mutations,
  actions,
  getters,
};
