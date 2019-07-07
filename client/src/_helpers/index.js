import axios from "axios";

function init_axios(token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export function validLink(link) {
  return link.substring(0, 4) === "http" ? link : `http://${link}`;
}

export async function initApp(store, token) {
  init_axios(token);
  await store.dispatch("students/getStudents");
  await store.dispatch("logs/getSessionTypes");
  await store.dispatch("logs/getSessionFeelings");
  await store.dispatch("logs/getLogs");
  await store.dispatch("options/getOptions");
}

export function runGoogleFormProcess(id) {
  const token = JSON.parse(localStorage.getItem("user")).token;
  axios.get(`http://127.0.0.1:8087/${id}?token=${token}`);
}
