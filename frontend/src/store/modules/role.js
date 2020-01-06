/* eslint-disable */
import request from '@/utils/request'


const state = {
  allRoles: null
};

const mutations = {
  SET_ALLROLES: (state, data) => {
    state.allRoles = data;
  },
};

const actions = {
  getAllRoles({commit}) {
    return new Promise(resolve => {
      request
      .get(`/role/get_all_roles/`)
      .then(response => {
        const { data } = response;
        commit('SET_ALLROLES', data)
        resolve(data)
      })
    })
  },

};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
