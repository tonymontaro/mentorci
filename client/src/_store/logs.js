import router from "../router";
import { logService } from "../_services";
import axios from "../_config";

export const logs = {
  namespaced: true,
  state: {
    logs: [],
    import: ""
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
      return newLog;
    },
    async updateLog({ commit }, log) {
      const updatedLog = await axios.put(`sessions/${log.id}/`, log);
      commit("updateLogSuccess", updatedLog);
      router.push("/sessions");
      return updatedLog;
    },
    async deleteLog({ commit }, log) {
      await axios.delete(`sessions/${log.id}/`);
      commit("deleteLogSuccess", log);
      router.push("/sessions");
      return log;
    }
  },
  mutations: {
    getLogsSuccess(state, logs) {
      logs.forEach(log => {
        log.durationInMins = Number(log.durationInMins);
      });
      state.logs = logs;
    },
    createLogSuccess(state, log) {
      log.durationInMins = Number(log.durationInMins);
      state.logs.unshift(log);
    },
    updateLogSuccess(state, log) {
      log.durationInMins = Number(log.durationInMins);
      state.logs = state.logs.map(lg => (lg.id == log.id ? log : lg));
    },
    deleteLogSuccess(state, log) {
      state.logs = state.logs.filter(lg => lg.id != log.id);
    },
    setImportText(state, importText) {
      state.import = importText;
    },
    reset(state) {
      state.logs = [];
    }
  }
};
