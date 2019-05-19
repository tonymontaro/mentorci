import router from "../router";
import { userService } from "../_services";

const user = JSON.parse(localStorage.getItem("user"));

export const authentication = {
  namespaced: true,
  state: user
    ? { status: { loggedIn: true }, user }
    : { status: {}, user: null },
  actions: {
    logout({ commit }) {
      userService.logout();
      commit("logout");
      router.push("/login");
    },
    login({ commit }, user) {
      userService
        .login(user)
        .then(user => {
          commit("loginSuccess", user);
          router.push("/");
        })
        .catch(error => {
          commit("loginFailure", error);
        });
    },
    signup({ commit }, user) {
      userService
        .signup(user)
        .then(user => {
          commit("loginSuccess", user);
          router.push("/");
        })
        .catch(error => {
          commit("loginFailure", error);
        });
    },
    updateMentor({ commit }, user) {
      userService
        .update(user)
        .then(user => {
          commit("loginSuccess", user);
        })
        .catch(error => {
          commit("loginFailure", error);
        });
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
      state.status = { error };
      state.user = null;
    }
  }
};
