import axios from "axios";
import jwt_decode from "jwt-decode";
import router from "../router";

function init_axios(token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export function validLink(link) {
  return link.substring(0, 4) === "http" ? link : `http://${link}`;
}

export async function initApp(store, token) {
  if (isTokenExpired()) {
    localStorage.clear();
    router.push("/login");
  } else {
    init_axios(token);
    await store.dispatch("students/getStudents");
    await store.dispatch("logs/getLogs");
    await store.dispatch("options/getOptions");
  }
}

export function runGoogleFormProcess(id) {
  const token = JSON.parse(localStorage.getItem("user")).token;
  axios.get(`http://127.0.0.1:8087/${id}?token=${token}`);
}

function isTokenExpired() {
  const token =
    JSON.parse(localStorage.getItem("user")) &&
    JSON.parse(localStorage.getItem("user"))["token"];
  if (!token || jwt_decode(token).exp < Date.now() / 1000) {
    return true;
  }
  return false;
}
