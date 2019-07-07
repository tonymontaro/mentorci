<template>
  <div class="container" v-if="student">
    <h3>
      {{ student.name }}
      <a href="#" @click="showEditStudentForm">
        <i class="fas fa-pencil-alt"></i>
      </a>
    </h3>
    <div v-show="!editStudentDetail">
      <p>Email: {{ student.email }}</p>
      <p>Stage: {{ student.stage }}</p>
      <p v-show="student.about">About: {{ student.about }}</p>
      <p>
        Github:
        <a target="_blank" :href="student.github | validLink">{{ student.github }}</a>
      </p>
      <p>Hours: {{hours}} ({{this.mins}} Mins)</p>
      <router-link class="btn" :to="{ name: 'log-form', params: { id: student.id } }">Log Session</router-link>
    </div>
    <div v-show="editStudentDetail" class="row">
      <form class="col s12" @submit.prevent="updateStudent">
        <div class="row">
          <div class="input-field col m6 s12">
            <input v-model="student.name" placeholder="Name" id="name" type="text" class="validate">
            <label class="active" for="name">Name</label>
          </div>
          <div class="input-field col m6 s12">
            <input
              v-model="student.email"
              id="email"
              type="email"
              class="validate"
              placeholder="email"
            >
            <label class="active" for="email">Email</label>
          </div>
        </div>
        <div class="row">
          <div class="input-field col m6 s12">
            <select v-model="student.stage">
              <option
                v-for="stage in $store.state.stages.stages"
                v-bind:key="stage"
                :value="stage"
              >{{ stage }}</option>
            </select>
            <label>Stage</label>
          </div>
          <div class="input-field col m6 s12">
            <input
              v-model="student.github"
              id="github"
              type="text"
              class="validate"
              placeholder="github"
            >
            <label class="active" for="github">github</label>
          </div>
        </div>
        <div class="row">
          <div class="input-field col s12">
            <textarea
              v-model="student.about"
              placeholder="About"
              id="studentAbout"
              class="materialize-textarea"
            ></textarea>
            <label class="active" for="studentAbout">About</label>
          </div>
        </div>
        <button class="btn">Save</button>
      </form>
    </div>
    <!-- Logs -->
    <h4>Logs</h4>
    <div class="row" v-if="logs.length > 0">
       <div class="col s12" v-for="log in logs" v-bind:key="log.id">
        <div class="card blue-grey darken-1 log-card">
          <div href="#" class="card-content white-text">
            <router-link
              :to="{ name: 'log-edit-form', params: { id: log.student, logid: log.id } }"
            >
              <span class="card-title">{{ log.id }} | Date: {{ log.date }}</span>
            </router-link>

            <p>
              
              <span class="yellow-text">Duration:</span>
              {{ parseInt(log.durationInMins) }}mins |
              <span class="yellow-text">Type:</span>
              {{log.types.split('|').join(', ')}} |
              <span class="yellow-text">Project(s):</span>
              {{log.projects}} 
            </p>
            <p>
              <span class="yellow-text">Summary:</span>
              {{ log.summary }}
            </p>
            <p v-if="log.concern">
              <span class="yellow-text">Concern:</span>
              {{ log.concern }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { validLink } from "../_helpers";

export default {
  name: "student-detail",
  data() {
    return {
      editStudentDetail: false
    };
  },
  mounted() {
    $("select").formSelect();
  },
  computed: {
    student() {
      let filtered = this.$store.state.students.students.filter(
        st => st.id == this.$route.params.id
      );
      if (filtered.length > 0) return filtered[0];
      return undefined;
    },
    logs() {
      let filtered = this.$store.state.logs.logs.filter(
        log => log.student == this.$route.params.id
      );
      if (filtered.length > 0) return filtered;
      return [];
    },
    mins() {
      return this.logs.reduce(
        (initial, val) => initial + val.durationInMins,
        0
      );
    },
    hours() {
      return (this.mins / 60).toFixed(2);
    }
  },
  methods: {
    async updateStudent() {
      const student = await this.$store.dispatch(
        "students/updateStudent",
        this.student
      );
      this.editStudentDetail = false;
    },
    showEditStudentForm() {
      this.editStudentDetail = !this.editStudentDetail;
    }
  },
  filters: {
    validLink
  }
};
</script>

<style>
i.fa-pencil-alt {
  font-size: 25px;
}
</style>
