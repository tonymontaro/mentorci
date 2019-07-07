import axios from "../_config";

export const options = {
  namespaced: true,
  state: {
    options: {}
  },
  actions: {
    async getOptions({ commit }) {
      const res = await axios.get(`sessions/options/`);
      commit("getOptionsSuccess", res.data);
      return res.data;
    }
  },
  mutations: {
    getOptionsSuccess(state, options) {
      state.options = options;
    }
  }
};