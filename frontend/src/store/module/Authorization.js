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
  // Sends a GET request to the api in order to get the JWT from google, using a one-time use google identity token
  // also sends a dispatch to check if the user is now logged in
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
  //Checks if a JWT is expired or is invalid, and if so logs the users out
  checkLoggedin({ commit, dispatch }) {
    const loggedIn = isLoggedIn();
    //checks if jwt is expired, logs you out if so
    if (getPayloadValue("exp") <= Date.now() / 1000) {
      dispatch("logout");
    } else {
      commit("setLoginData", loggedIn);
    }
  },

  // Requests a pusher-specific token to authenticate the user to a pusher-channel, this ensures only the authenticated user can see messages from specific channel(s)
  authenticatePusher({ commit }) {
    Pusher.logToConsole = false;

    const authUrl = `${process.env.VUE_APP_PROCESSING_ENDPOINT}/auth/pusher`;
    let authorizer = (channel) => {
      return {
        authorize: (socketId, callback) => {
          const body = JSON.stringify({
            socket_id: socketId,
            channel_name: channel.name,
          });
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
