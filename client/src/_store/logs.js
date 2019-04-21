import router from "../router";
import { logService } from "../_services";
import axios from "axios";
import config from "../_config";

export const logs = {
  namespaced: true,
  state: {
    logs: [],
    sessionTypes: [],
    sessionFeelings: []
  },
  actions: {
    async getLogs({ commit }) {
      const logs = await logService.getLogs();
      commit("getLogsSuccess", logs);
      return logs;
    },
    async createLog({ commit }, log) {
      const newLog = await logService.createLog(log);
      commit("createLogSuccess", newLog);
      router.push("/sessions");
      return newLog;
    },
    async updateLog({ commit }, log) {
      const updatedLog = await axios.put(
        `${config.apiUrl}sessions/${log.id}/`,
        log
      );
      commit("updateLogSuccess", updatedLog);
      router.push("/sessions");
      return updatedLog;
    },
    async deleteLog({ commit }, log) {
      await axios.delete(`${config.apiUrl}sessions/${log.id}/`);
      commit("deleteLogSuccess", log);
      router.push("/sessions");
      return log;
    },
    async getSessionTypes({ commit }) {
      const res = await axios.get(`${config.apiUrl}sessions/types/`);
      commit("getSessionTypesSuccess", res.data);
    },
    async getSessionFeelings({ commit }) {
      const res = await axios.get(`${config.apiUrl}sessions/feelings/`);
      commit("getSessionFeelingsSuccess", res.data);
    }
  },
  mutations: {
    getLogsSuccess(state, logs) {
      state.logs = logs;
    },
    createLogSuccess(state, log) {
      state.logs.unshift(log);
    },
    updateLogSuccess(state, log) {
      state.logs = state.logs.map(lg => (lg.id == log.id ? log : lg));
    },
    deleteLogSuccess(state, log) {
      state.logs = state.logs.filter(lg => lg.id != log.id);
    },
    getSessionTypesSuccess(state, sessionTypes) {
      state.sessionTypes = sessionTypes;
    },
    getSessionFeelingsSuccess(state, sessionFeelings) {
      state.sessionFeelings = sessionFeelings;
    }
  }
};
