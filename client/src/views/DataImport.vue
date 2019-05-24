<template>
  <div class="container">
    <h4 class="center">Import Data</h4>

    <form @submit.prevent="importData">
      <div class="input-field">
        <textarea id="dataFromApi" v-model="dataFromApi" class="materialize-textarea" required></textarea>
        <label for="dataFromApi" class="active">Paste in data from the Google Script API here</label>
      </div>
      <div class="log-buttons right">
        <button class="btn">Import</button>
      </div>
    </form>

    <div class="error-msg" v-show="message">
      <div v-html="message"></div>
      <router-link class="btn right" to="/">View/Edit Students</router-link>
      <CreateStudentModal/>&nbsp;
    </div>
  </div>
</template>


<script>
import { initApp } from "../_helpers";
import CreateStudentModal from "./components/CreateStudentModal.vue";

export default {
  components: {
    CreateStudentModal
  },
  data() {
    return {
      dataFromApi: this.$store.state.logs.import,
      data: undefined,
      message: ""
    };
  },
  mounted() {
    const user = this.$store.state.authentication.user;
    if (user && this.$store.state.students.students.length == 0) {
      initApp(this.$store, user.token);
    }
  },
  computed: {
    studentMap() {
      const students = {};
      this.$store.state.students.students.forEach(st => {
        students[st.name] = st;
      });
      return students;
    }
  },
  methods: {
    importData() {
      this.$store.commit("logs/setImportText", this.dataFromApi);
      this.data = JSON.parse(this.dataFromApi);
      const unknownStudents = [];
      this.data.details.forEach(data => {
        if (!this.studentMap[data.student_name]) {
          unknownStudents.push(data.student_name);
        }
      });
      if (unknownStudents.length == 0) {
        this.message = "";
        this.data.details.forEach(async data => {
          const [day, month, year] = data.date.split("/");
          let [hours, mins, secs] = data.duration.split(":");
          hours = hours.length == 1 ? "0" + hours : hours;
          const log = {
            student: this.studentMap[data.student_name].id,
            mentor: this.$store.state.authentication.user.id,
            date: `${year}-${month}-${day}`,
            duration: `${hours}-${mins}-${secs}`,
            types: "other",
            concern: "",
            summary: "imported",
            feeling: "average"
          };
          await this.$store.dispatch("logs/createLog", log);
        });
        this.dataFromApi = "";
        this.$store.commit("logs/setImportText", this.dataFromApi);
        this.message = `<h2 class="green-text">Success!<h2>`;
      } else {
        this.message = `
        <p class="red-text">The following Student Name(s) were not found.<p>
        <p><b>${unknownStudents.join("<br />")}</b><p>
        <p>Please create a profile (or edit the name) for each listed student.</p>`;
      }
    }
  }
};
</script>

<style>
.error-msg #add-student {
  margin-top: 0;
}
</style>

