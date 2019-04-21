import axios from "axios";
import config from "../_config";

export const stages = {
  namespaced: true,
  state: {
    stages: []
  },
  actions: {
    async getStages({ commit }) {
      const res = await axios.get(`${config.apiUrl}students/stages/`);
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
