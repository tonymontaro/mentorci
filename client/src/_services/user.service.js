import axios from "axios";
import config from "../_config";

function login(user) {
  return axios.post(`${config.apiUrl}auth/login/`, user).then(res => {
    localStorage.setItem("user", JSON.stringify(res.data));
    return res.data;
  });
}

function signup(user) {
  return axios.post(`${config.apiUrl}auth/register/`, user).then(res => {
    localStorage.setItem("user", JSON.stringify(res.data));
    return res.data;
  });
}

function logout() {
  localStorage.removeItem("user");
}

export const userService = {
  logout,
  login,
  signup
};
