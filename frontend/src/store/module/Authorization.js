import { isLoggedIn, logoutCookie, getCookie, getPayloadValue } from "@/util/Cookie";
import Pusher from "pusher-js";

const state = {
  loggedIn: false,
  jwt: "",
  pusher: null,
};

const mutations = {
  setLoginData: (state, login) => (state.loggedIn = login),
  setJwtData: (state, jwt) => (state.jwt = jwt),
  setPusherSession: (state, pusher) => (state.pusher = pusher),
};
const actions = {
  async login({ dispatch }, { routeCode }) {
    const response = await fetch(process.env.VUE_APP_PROCESSING_ENDPOINT + "/auth?code=" + routeCode, {
      method: "GET",
    });

    const json = await response.json();

    if (json["jwt"].length > 0) {
      document.cookie = "jwt=" + json["jwt"];
      document.cookie = "loggedIn=" + "true";
    }

    dispatch("checkLoggedin");
  },
  logout({ dispatch }) {
    logoutCookie();
    dispatch("checkLoggedin");
  },
  checkLoggedin({ commit, dispatch }) {
    const loggedIn = isLoggedIn();
    //checks if jwt is expired, logs you out if so
    if (getPayloadValue("exp") <= (Date.now() / 1000)) {
      dispatch("logout")
    } else {
      commit("setLoginData", loggedIn);
    }
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
            headers: {
              "Content-Type": "application/json",
              Authorization: jwt,
            },
            body: body,
          })
            .then((res) => {
              if (!res.ok) {
                throw new Error(`Received ${res.statusCode} from ${authUrl}`);
              }

              return res.json();
            })
            .then((data) => {
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
  pusherSession: (state) => state.pusher,
};

export default {
  state,
  namespaced: true,
  mutations,
  actions,
  getters,
};
