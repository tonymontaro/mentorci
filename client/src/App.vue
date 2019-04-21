<template>
  <div id="app">
    <header>
      <div id="nav" class="center-align">
        <router-link to="/">Home |&nbsp;</router-link>
        <router-link to="/sessions">Sessions |&nbsp;</router-link>
        <router-link to="/profile">Profile |&nbsp;</router-link>
        <router-link v-if="!$store.state.authentication.user" to="/login">Login</router-link>
        <a href="#" @click="logout" v-else>Logout</a>
      </div>
    </header>
    <router-view/>
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

export default {
  name: "app",
  created() {
    const user = this.$store.state.authentication.user;
    if (user && this.$store.state.students.students.length == 0) {
      initApp(this.$store, user.token);
    }
  },
  methods: {
    logout() {
      this.$store.dispatch("authentication/logout");
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
}
footer {
  padding: 30px 0;
}
</style>
