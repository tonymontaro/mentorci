<template>
  <div class="home container" v-if="this.$store.state.authentication.user">
    <div class="input-field">
      <input type="text" placeholder="Search..." v-model="search">
    </div>

    <div class="row">
      <div class="col s12 m4" v-for="student in students" v-bind:key="student.id">
        <div class="card blue-grey darken-1 student-card">
          <div href="#" class="card-content white-text">
            <span class="card-title">
              <router-link
                :to="{ name: 'student-detail', params: { id: student.id } }"
              >{{ student.name | truncateCardText(19) }}</router-link>
            </span>
            <p>
              <i class="far fa-envelope"></i>
              {{ student.email | truncateCardText }}
            </p>
            <p>
              <i class="far fa-clock"></i>
              {{ student.stage | truncateCardText }}
            </p>
            <p>
              <i class="fab fa-github"></i>
              <a :href="student.github | validLink" target="_blank">GitHub</a>
            </p>
          </div>
          <div class="card-action">
            <router-link :to="{ name: 'student-detail', params: { id: student.id } }">View</router-link>
            <router-link :to="{ name: 'log-form', params: { id: student.id } }">Log Session</router-link>
          </div>
        </div>
      </div>
    </div>
    <h5>total: {{ students.length }}</h5>

    <a class="waves-effect waves-light btn modal-trigger" href="#addStudent" id="add-student">
      <i class="fas fa-plus"></i>Add Student
    </a>
    <div class="clear-fix"></div>

    <!-- Add Student Modal -->
    <div id="addStudent" class="modal">
      <div class="modal-content">
        <div class="row">
          <form class="col s12" @submit.prevent="createStudent">
            <h4 class="center">Add Student</h4>
            <div class="row">
              <div class="input-field col m6 s12">
                <input
                  v-model="newStudent.name"
                  placeholder="Name"
                  id="student-name"
                  type="text"
                  class="validate"
                >
                <label class="active" for="student-name">Name*</label>
              </div>
              <div class="input-field col m6 s12">
                <input
                  v-model="newStudent.email"
                  id="student-email"
                  type="email"
                  class="validate"
                  placeholder="email"
                  required
                >
                <label class="active" for="student-email">Email*</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col m6 s12">
                <select v-model="newStudent.stage">
                  <option v-for="stage in stages" v-bind:key="stage" :value="stage">{{ stage }}</option>
                </select>
                <label>Stage</label>
              </div>
              <div class="input-field col m6 s12">
                <input
                  v-model="newStudent.github"
                  id="github"
                  type="text"
                  class="validate"
                  placeholder="github"
                >
                <label class="active" for="github url">GitHub Url</label>
              </div>
            </div>
            <div class="input-field">
              <button href="#!" class="btn right">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { validLink } from "../_helpers";
import { initApp } from "../_helpers";

export default {
  name: "home",
  data() {
    return {
      search: "",
      newStudent: {
        name: "",
        email: "",
        stage: "",
        mentor: this.$store.state.authentication.user.id,
        github: ""
      }
    };
  },
  async mounted() {
    $(".modal").modal();
    if (this.$store.state.stages.stages.length == 0)
      await this.$store.dispatch("stages/getStages");
    $("select").formSelect();
    const user = this.$store.state.authentication.user;
    if (user && this.$store.state.students.students.length == 0) {
      initApp(this.$store, user.token);
    }
  },
  computed: {
    stages() {
      return this.$store.state.stages.stages;
    },
    students() {
      let result = this.$store.state.students.students;
      if (!this.search) return result;
      result = result.filter(student => {
        const searchTerm = this.search.toLowerCase();
        return (
          student.name.toLowerCase().includes(searchTerm) ||
          student.stage.toLowerCase().includes(searchTerm) ||
          student.email.toLowerCase().includes(searchTerm)
        );
      });
      return result;
    }
  },
  methods: {
    async createStudent() {
      await this.$store.dispatch("students/createStudent", this.newStudent);
      $(".modal").modal("close");
    }
  },
  filters: {
    truncateCardText(word, num = 25) {
      return word.length > num ? word.slice(0, num - 2) + " ..." : word;
    },
    validLink
  }
};
</script>

<style>
.card,
.card .card-action:last-child {
  border-radius: 15px;
}
.card-content a {
  color: #fff;
  border-bottom: 1px #fff solid;
}
#add-student {
  float: right;
  font-size: 16px;
}
#add-student i {
  margin-right: 8px;
}
.card .card-content p {
  margin-bottom: 5px;
}
.clear-fix {
  clear: both;
}
.student-card .card-content {
  padding-bottom: 0px;
}
.student-card i {
  margin-right: 8px;
  font-size: 18px;
}
/* .home select {
  display: block;
} */
</style>
