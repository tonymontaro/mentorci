import axios from "../_config";

async function getLogs() {
  const res = await axios.get("sessions/");
  return res.data;
}

async function createLog(log) {
  const res = await axios.post("sessions/", log);
  return res.data;
}

export const logService = {
  getLogs,
  createLog
};
