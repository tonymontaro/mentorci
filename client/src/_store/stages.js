import axios from "../_config";

export const stages = {
  namespaced: true,
  state: {
    stages: []
  },
  actions: {
    async getStages({ commit }) {
      const res = await axios.get(`students/stages/`);
      commit("getStagesSuccess", res.data);
      return res.data;
    }
  },
  mutations: {
    getStagesSuccess(state, stages) {
      state.stages = stages;
    }
  }
};
