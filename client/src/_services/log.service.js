import axios from "axios";
import config from "../_config";

async function getLogs() {
  const res = await axios.get(`${config.apiUrl}sessions/`);
  return res.data;
}

async function createLog(log) {
  const res = await axios.post(`${config.apiUrl}sessions/`, log);
  return res.data;
}

export const logService = {
  getLogs,
  createLog
};
