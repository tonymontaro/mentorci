let root = "";
if (process.env.NODE_ENV === "development") root = "http://127.0.0.1:8000";

export default {
  apiUrl: root + "/api/v1/"
};
