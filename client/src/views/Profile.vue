<template>
  <div class="container" v-if="this.$store.state.authentication.user">
    <h3>{{ this.$store.state.authentication.user.fullname }}</h3>
    <h5>Email: {{ this.$store.state.authentication.user.email }}</h5>
    <p>
      <b>Bio:</b>
      <br />
      {{ this.$store.state.authentication.user.bio || "None." }}
    </p>
    <hr />
    <p>ID: {{ this.$store.state.authentication.user.id }}</p>
  </div>
</template>
