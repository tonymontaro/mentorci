import Vue from "vue";
import Vuex from "vuex";

import { authentication } from "./authentication";
import { students } from "./students";
import { stages } from "./stages";
import { logs } from "./logs";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    authentication,
    students,
    stages,
    logs
  },
  actions: {
    clearAll({ commit }) {
      commit("students/reset");
      commit("logs/reset");
    }
  }
});
