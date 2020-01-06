/* eslint-disable */
const state = {
  ActivateLightTheme: false,
  alertInfo: { props: { value: false }, defaultSlot: "" }
};

const mutations = {
  SET_ACTIVATELIGHTTHEME: (state, ActivateLightTheme) => {
    state.ActivateLightTheme = ActivateLightTheme;
  },
  SET_TOGGLE_ALERTVALUE: (state, value) => {
    state.alertInfo.props.value = value;
  },
  SET_ALERTINFO: (state, alertInfo) => {
    state.alertInfo = alertInfo;
  }
};

const actions = {
  changeTheme({ commit, state }) {
    if (state.ActivateLightTheme == true) {
      commit("SET_ACTIVATELIGHTTHEME", false);
    } else if (state.ActivateLightTheme == false) {
      commit("SET_ACTIVATELIGHTTHEME", true);
    }
  },
  toggleAlertValue({ commit, state }) {
    commit("SET_TOGGLE_ALERTVALUE", !state.alertInfo.props.value);
  },
  changeAlertInfo({ commit, state }, { props, defaultSlot }) {
    let toggleAlertValue = Object.assign(
      {},
      { dismissible: true, value: true },
      props
    );
    commit("SET_ALERTINFO", { props: toggleAlertValue, defaultSlot });
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
