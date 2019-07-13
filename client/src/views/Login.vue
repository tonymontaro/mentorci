<template>
  <div class="container">
    <h2>Login</h2>
    <form @submit.prevent="login" v-show="showSignIn" id="loginForm">
      <div class="form-group">
        <label for="login-email">Email</label>
        <input type="text" v-model="email" name="email" id="login-email" class="form-control" />
      </div>
      <div class="form-group">
        <label for="login-password">Password</label>
        <input
          type="password"
          v-model="password"
          id="login-password"
          name="password"
          class="form-control"
        />
      </div>
      <p>
        <a href="#" @click="toggleSignIn">Sign Up?</a>
      </p>
      <div class="form-group">
        <button class="btn">Login</button>
      </div>
    </form>

    <form @submit.prevent="signup" v-show="!showSignIn" id="signupForm">
      <div class="form-group">
        <label for="signup-email">Email*</label>
        <input
          type="email"
          v-model="email"
          name="email"
          id="signup-email"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="signup-fullname">Full Name*</label>
        <input
          type="text"
          v-model="fullname"
          name="fullname"
          id="signup-fullname"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="signup-password">Password*</label>
        <input
          type="password"
          v-model="password"
          id="signup-password"
          name="password"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="signup-bio">Bio</label>
        <textarea v-model="bio" name="signup-bio" id="bio" class="materialize-textarea"></textarea>
      </div>
      <p>
        <a href="#" @click="toggleSignIn">Sign In?</a>
      </p>
      <div class="form-group">
        <button class="btn">Register</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      fullname: "",
      bio: "",
      showSignIn: true
    };
  },
  methods: {
    login() {
      const { email, password } = this;
      if (email && password) {
        this.$store.dispatch("authentication/login", { email, password });
      }
    },
    signup() {
      const { email, password } = this;
      if (email && password) {
        const user = {
          email,
          password,
          bio: this.bio,
          fullname: this.fullname
        };
        this.$store.dispatch("authentication/signup", user);
      }
    },
    toggleSignIn() {
      this.showSignIn = !this.showSignIn;
    }
  }
};
</script>
