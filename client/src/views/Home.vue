<template>
  <div class="home container" v-if="this.$store.state.authentication.user">
    <div class="row">
      <div class="col m9 s12">
        <div class="input-field">
          <div class="row">
            <div class="col s9">
              <input type="text" placeholder="Search..." v-model="search" />
            </div>
            <div class="col s3 hide-on-med-and-up">
              <button class="btn student-search">
                <i class="fas fa-search"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      <CreateStudentModal />
    </div>

    <div class="row">
      <div class="col s12 l4 m6" v-for="student in students" v-bind:key="student.id">
        <div class="card blue-grey darken-1 student-card" :testid="student.name">
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

    <div class="fixed-action-btn">
      <a class="btn-floating btn-large" href="#pageTop">
        <i class="fas fa-chevron-up"></i>
      </a>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { validLink } from "../_helpers";
import { initApp } from "../_helpers";
import CreateStudentModal from "./components/CreateStudentModal.vue";

export default {
  name: "home",
  components: {
    CreateStudentModal
  },
  data() {
    return {
      search: ""
    };
  },
  async mounted() {
    const user = this.$store.state.authentication.user;
    if (user && this.$store.state.students.students.length == 0) {
      initApp(this.$store, user.token);
    }
  },
  computed: {
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
  margin-top: 20px;
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
body {
  padding-top: 50px;
}
.student-card .card-title,
.student-card p {
  white-space: nowrap;
  overflow: hidden;
}
.student-search {
  margin-top: 5px;
}
</style>
