<template>
  <div class="col m3 s12">
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
export default {
  name: "create-student-modal",
  data() {
    return {
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
  },
  computed: {
    stages() {
      return this.$store.state.stages.stages;
    }
  },
  methods: {
    async createStudent() {
      try {
        await this.$store.dispatch("students/createStudent", this.newStudent);
        $(".modal").modal("close");
      } catch {
        alert("Invalid Student details. Email may already exist.");
      }
    }
  }
};
</script>
