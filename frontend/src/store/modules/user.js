/* eslint-disable */
import request from "@/utils/request";
import qs from "qs";

const state = {
  token: null,
  username: "",
  truename: "",
  userRoles: null,
  allUsers: [],
  userRoutes: [],
  userSidebarRoutes: []
};

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token;
  },
  SET_USERNAME: (state, username) => {
    state.username = username;
  },
  SET_TRUENAME: (state, truename) => {
    state.truename = truename;
  },
  SET_ALLUSERS: (state, data) => {
    state.allUsers = data;
  },
  SET_USERROLES: (state, data) => {
    state.userRoles = data;
  },
  SET_USERROUTES: (state, data) => {
    state.userRoutes = data;
  },
  SET_USERSIDEBARROUTES: (state, data) => {
    state.userSidebarRoutes = data;
  }
};


function extract_route_info({routes, userRoles}) {
  return routes.map(function(route) {
    let routeInfo = {};
    routeInfo.name = route.name;


    // flatten meta up if meta exists
    if (Object.keys(route).includes("meta")) {
      // if roles required for route, check it
      if (route.meta.roles) {
        let roles_intersection = route.meta.roles.filter(function(role) {
          return userRoles.indexOf(role) !== -1;
        });
        // if have required role then add it
        if (roles_intersection.length > 0) {
          Object.assign(routeInfo, route.meta);
        } else {
          return null
        }
      // if no roles required just add it
      } else {
        Object.assign(routeInfo, route.meta);
      }
    // if no meta, it implicts no roles required, just add it
    } else {
      Object.assign(routeInfo, route.meta);
    }

    // // flatten meta up if meta exists
    // if (Object.keys(route).includes("meta")) {
    //   Object.assign(routeInfo, route.meta);
    // }
    // // if roles required for route, check it
    // if (routeInfo.roles) {
    //   let roles_intersection = routeInfo.roles.filter(function(role) {
    //     return userRoles.indexOf(role) !== -1;
    //   });
      

    //   if (!roles_intersection.length) {
    //     return null;
    //   }
    // }
    // don't include children if don't have required role
    // when user doesn't have require roles for child, child's child is ignored in this case
    if (route.children) {
      let routeChildrenInfo = extract_route_info({routes: route.children, userRoles: userRoles});
      if (routeChildrenInfo.length) {
        routeInfo.children = routeChildrenInfo;
      }
    }

    return routeInfo;
  })
  .filter(info => info); // remove null; e.g, user don't have roles required
};

const actions = {
  getToken({ commit, state }, payload) {
    return new Promise((resolve, reject) => {
      request
        .post(`/login/access-token`, qs.stringify(payload), {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
          }
        })
        .then(response => {
          const { data } = response;

          const { access_token } = data;

          localStorage.setItem("token", access_token);
          commit("SET_TOKEN", access_token);
          resolve(access_token);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  getUsername({ commit }) {
    return new Promise((resolve, reject) => {
      request
        .get(`/user/me`)
        .then(response => {
          const { data } = response;

          const { AdminName, TrueName } = data;

          commit("SET_USERNAME", AdminName);
          commit("SET_TRUENAME", TrueName);
          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  getUserRoles({ commit, state }) {
    return new Promise(resolve => {
      request
        .get(`/perm/get_roles_for_user`, {
          params: { user: state.username }
        })
        .then(response => {
          const { data } = response;
          commit("SET_USERROLES", data);
          resolve(data);
        });
    });
  },
  async login({ dispatch }, {playload, routes}) {
    
    await dispatch("getToken", playload);
    await dispatch("getUsername");
    await dispatch("getUserRoles");
    await dispatch("getRoutesForUser", {routes})
    await dispatch("getSidebarRoutesForUser", {routes})
  },
  logout({ commit }) {
    return new Promise(resolve => {
      localStorage.removeItem("token");
      commit("SET_TOKEN", null);
      commit("SET_USERNAME", null);
      commit("SET_TRUENAME", null);
      commit("SET_USERROLES", null);
      commit("SET_USERROUTES", null);
      resolve();
    });
  },
  getAllUsers({ commit }) {
    return new Promise(resolve => {
      request.get(`/user/read_users/`).then(response => {
        const { data } = response;
        commit("SET_ALLUSERS", data);
        resolve(data);
      });
    });
  },
  getRoutesForUser({ commit, state}, {routes}) {
    let userRoutes = extract_route_info({routes: routes, userRoles: state.userRoles})
    commit("SET_USERROUTES", userRoutes);
  },
  async getSidebarRoutesForUser({ commit, dispatch, state }, {routes}) {
    let sidebarRoutes = routes.filter(function(route) {
      return route.meta && route.meta.inSidebar;
    });

    let userRoutesInfo = extract_route_info({routes: sidebarRoutes, userRoles: state.userRoles});

    let result;

    if (userRoutesInfo.length === 1) {
      result = userRoutesInfo[0].children;
    }

    // console.log('sidebarRoutes', sidebarRoutes)
    
    commit("SET_USERSIDEBARROUTES", result);
  }
  // REGISTER: ({ commit }, { username, email, password }) => {
  //   return new Promise((resolve, reject) => {
  //     request
  //       .post(`register`, {
  //         username,
  //         email,
  //         password
  //       })
  //       .then(({ data, status }) => {
  //         if (status === 201) {
  //           resolve(true);
  //         }
  //       })
  //       .catch(error => {
  //         reject(error);
  //       });
  //   });
  // },
  // REFRESH_TOKEN: () => {
  //   return new Promise((resolve, reject) => {
  //     request
  //       .post(`token/refresh`)
  //       .then(response => {
  //         resolve(response);
  //       })
  //       .catch(error => {
  //         reject(error);
  //       });
  //   });
  // }
};


export default {
  namespaced: true,
  state,
  mutations,
  actions
};
