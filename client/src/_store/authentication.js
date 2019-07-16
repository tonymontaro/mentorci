import axios from "../_config";
import router from "../router";
const user = JSON.parse(localStorage.getItem("user"));

export const authentication = {
  namespaced: true,
  state: user
    ? { status: { loggedIn: true }, user }
    : { status: {}, user: null },
  actions: {
    logout({ commit }) {
      localStorage.removeItem("user");
      commit("logout");
      router.push("/login");
    },
    async login({ commit }, user) {
      const userData = (await axios.post(`auth/login/`, user)).data;
      localStorage.setItem("user", JSON.stringify(userData));
      commit("loginSuccess", userData);
      router.push("/");
    },
    async signup({ commit }, user) {
      const userData = (await axios.post(`auth/register/`, user)).data;
      localStorage.setItem("user", JSON.stringify(userData));
      commit("loginSuccess", userData);
      router.push("/");
    },
    async updateMentor({ commit }, user) {
      const userData = (await axios.put(`mentors/${user.id}/`, user)).data;
      localStorage.setItem("user", JSON.stringify(userData));
      commit("loginSuccess", user);
    }
  },
  mutations: {
    logout(state) {
      state.status = {};
      state.user = null;
    },
    loginSuccess(state, user) {
      state.status = { loggedIn: true };
      state.user = user;
    },
    loginFailure(state, error) {
      alert("Invalid Login/Registration details.");
      state.status = { error };
      state.user = null;
    }
  }
};
