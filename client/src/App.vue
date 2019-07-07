<template>
  <div id="app">
    <header>
      <div id="nav" class="center-align">
        <div v-if="$store.state.authentication.user">
          <router-link to="/">Home |&nbsp;</router-link>
          <router-link to="/sessions">Sessions |&nbsp;</router-link>
          <router-link to="/profile">Profile |&nbsp;</router-link>
          <router-link to="/import">Import&nbsp;</router-link>
        </div>
        <div v-else>
          <router-link to="/login">Login/Register</router-link>
        </div>
      </div>
      <loader v-show="$store.state.loader.asyncCalls > 0"></loader>
    </header>
    <router-view />
    <footer>
      <div class="container">
        <i class="fas fa-mug-hot"></i> By
        <a target="_blank" href="https://www.linkedin.com/in/anthonyngene/">tonymontaro</a>. Project available
        <a
          href="https://github.com/tonymontaro/mentorci"
          target="_blank"
        >on github</a>
      </div>
    </footer>
  </div>
</template>

<script>
import { initApp } from "./_helpers";
import loader from "./views/components/loader.vue";

export default {
  name: "app",
  components: {
    loader
  },
  async created() {
    const user = this.$store.state.authentication.user;
    if (user && this.$store.state.students.students.length == 0) {
      await initApp(this.$store, user.token);
      $("select").formSelect();
      $(".modal").modal();
    }
  }
};
</script>

<style lang="scss">
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }

  position: fixed;
  width: 100%;
  height: 50px;
  top: 0;
  z-index: 999;
  background: white;
  padding: 15px;
  border-bottom: 1px solid #a1a1a1;
}
footer {
  padding: 30px 0;
}
</style>
