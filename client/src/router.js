import Vue from "vue";
import Router from "vue-router";
import jwt_decode from "jwt-decode";
import Home from "./views/Home.vue";
import Login from "./views/Login.vue";
import Logs from "./views/Logs.vue";
import Profile from "./views/Profile.vue";
import StudentDetail from "./views/StudentDetail.vue";
import LogForm from "./views/LogForm.vue";
import DataImport from "./views/DataImport.vue";
import store from "./_store";

Vue.use(Router);

const router = new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/login",
      name: "login",
      component: Login
    },
    {
      path: "/students/:id",
      name: "student-detail",
      component: StudentDetail
    },
    {
      path: "/sessions",
      name: "sessions",
      component: Logs
    },
    {
      path: "/students/:id/log",
      name: "log-form",
      component: LogForm
    },
    {
      path: "/students/:id/log/:logid",
      name: "log-edit-form",
      component: LogForm
    },
    {
      path: "/profile",
      name: "profile",
      component: Profile
    },
    {
      path: "/import",
      name: "import",
      component: DataImport
    },
    {
      path: "*",
      name: "home",
      component: Home
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.fullPath !== "/login") {
    if (!store.state.authentication.user || isTokenExpired()) {
      localStorage.clear();
      return next("/login");
    }
  }
  next();
});

function isTokenExpired() {
  const token =
    JSON.parse(localStorage.getItem("user")) &&
    JSON.parse(localStorage.getItem("user"))["token"];
  if (!token || jwt_decode(token).exp < Date.now() / 1000) {
    return true;
  }
  return false;
}

export default router;
