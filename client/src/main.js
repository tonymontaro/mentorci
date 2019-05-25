import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./_store";

Vue.config.productionTip = false;

const errorMsg =
  ".<br/> Possible reasons; 1. Invalid data supplied 2. Email already exist. 3. Missing field(s)";
window.addEventListener("unhandledrejection", function(event) {
  alert(event.reason + errorMsg);
});

Vue.config.errorHandler = function(err) {
  alert(err + errorMsg);
};

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
