import axios from "../_config";

function login(user) {
  return axios.post(`auth/login/`, user).then(res => {
    localStorage.setItem("user", JSON.stringify(res.data));
    return res.data;
  });
}

function signup(user) {
  return axios.post(`auth/register/`, user).then(res => {
    localStorage.setItem("user", JSON.stringify(res.data));
    return res.data;
  });
}

function update(user) {
  return axios.put(`mentors/${user.id}/`, user).then(res => {
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
  signup,
  update
};
