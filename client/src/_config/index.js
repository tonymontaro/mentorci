let root = "";
if (process.env.NODE_ENV === "development") root = "http://127.0.0.1:8000";

export default {
  apiUrl: root + "http://35.181.102.147/api/v1/"
};
