import axios from "axios";
import store from "../_store";

let apiUrl = "https://api.mentorci.online/api/v1";
if (process.env.NODE_ENV === "development")
  apiUrl = "http://127.0.0.1:8000/api/v1/";

const instance = axios.create({
  baseURL: apiUrl,
});

instance.interceptors.request.use((config) => {
  store.commit("loader/increment");
  return config;
});

instance.interceptors.response.use(
  (response) => {
    store.commit("loader/decrement");
    return response;
  },
  (error) => {
    store.commit("loader/decrement");
    throw error;
  }
);

export default instance;
