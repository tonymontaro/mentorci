let rootUrl = "https://api.mentorci.ga/api/v1/";
if (process.env.NODE_ENV === "development")
  rootUrl = "http://127.0.0.1:8000/api/v1/";

export default {
  apiUrl: rootUrl
};
