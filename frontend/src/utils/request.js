import axios from "axios";

import router from "@/router";
import store from "@/store";

// create an axios instance
const service = axios.create({
  //baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  baseURL: process.env.VUE_APP_BASE_API, // "http://localhost:8000/api/v1/",
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 1000 * 60 * 10 // request timeout
});

// add token before every request if there is token in localStorage
service.interceptors.request.use(
  config => {
    let token = localStorage.getItem("token");

    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }

    return config;
  },

  error => {
    console.log("error in service.interceptors.request.use"); // for debug
    return Promise.reject(error);
  }
);

service.interceptors.response.use(
  response => {
    return response;
  },
  async function(error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      const {
        config,
        response: { status, data }
      } = error;

      const originalRequest = config;

      console.log("in interceptors", JSON.stringify(error));

      // redict to login page no token provided in header
      if (data.detail === "Not authenticated") {
        router.push({ name: "login" });
        return Promise.reject(false);
      }

      // keep reject when failed to get a new token
      if (originalRequest.url.includes(`login/access-token`)) {
        return Promise.reject(error);
      }

      // redict to login page if exists but can't validate
      // this may happen when the backend change secert key of jwt
      if (status === 401 && data.detail === "Could not validate credentials") {
        console.log(
          'status === 401 && data.detail === "Could not validate credentials"'
        );
        store.dispatch("user/logout");
        router.push({ name: "login" });
        return Promise.reject(error);
      }

      // redict to login page if token expires
      if (status === 401 && data.detail === "Expired token") {
        console.log('status === 401 && data.detail === "Expired token"');
        // check https://github.com/konshensx16/vue-todo-frontend/blob/master/src/main.js when there is need to use refresh token
        router.push({ name: "login" });
        return Promise.reject(error);
      }

      // redict to login page if token expires
      if (status === 403 && data.detail === "No permission") {
        console.log('status === 401 && data.detail === "No permission"');
        // check https://github.com/konshensx16/vue-todo-frontend/blob/master/src/main.js when there is need to use refresh token
        router.push({ name: "NoPermission" });
        return Promise.reject(error);
      }
    } else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      console.log("The request was made but no response was received");
      console.log(error.toJSON());
      if (error.message !== "Request aborted") {
        await store.dispatch("app/changeAlertInfo", {
          props: { type: "error", dismissible: true },
          defaultSlot:
            "对不起，出错了。" +
            "Info: error.request " +
            "Detail: " +
            JSON.stringify(error.message)
        });
      }

      return Promise.reject(error);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log(
        "Something happened in setting up the request that triggered an Error"
      );
      await store.dispatch("app/changeAlertInfo", {
        props: { type: "error", dismissible: true },
        defaultSlot:
          "Sorry, there is an error." +
          "Info: setting up the request " +
          "Detail: " +
          JSON.stringify(error.message)
      });
      return Promise.reject(error);
    }
  }
);

export default service;
