import Vue from "vue";
import Vuex from "vuex";

import { authentication } from "./authentication";
import { students } from "./students";
import { stages } from "./stages";
import { options } from "./options";
import { logs } from "./logs";
import { loader } from "./loader";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    authentication,
    students,
    stages,
    logs,
    loader,
    options
  },
  actions: {
    clearAll({ commit }) {
      commit("students/reset");
      commit("logs/reset");
    }
  }
});
