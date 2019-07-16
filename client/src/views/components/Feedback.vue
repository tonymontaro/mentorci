// Todo: Add E2E test for Feedback feature

<template>
  <div>
    <a class="waves-effect waves-light btn modal-trigger" href="#addFeedback" id="add-student">
      <i class="fas fa-plus"></i>Add Feedback
    </a>
    <hr />
    <div class="col s12" v-for="feedback in feedbackList" v-bind:key="feedback.id">
      <div class="card blue-grey darken-1 log-card">
        <div href="#" class="card-content white-text">
          <span class="card-title">{{feedback.project}} : {{ parseInt(feedback.score) }}%</span>

          <p>
            <span class="yellow-text">Summary:</span>
            {{ feedback.summary }}
            <button
              @click="deleteFeedback(feedback.id)"
              class="btn btn-sm right"
            >Delete</button>
          </p>
        </div>
      </div>
    </div>
    <!-- Add Feedback Modal col m3 s12 -->
    <div id="addFeedback" class="modal">
      <div class="modal-content">
        <div class="row">
          <form class="col s12" @submit.prevent="createFeedback" id="createFeedbackForm">
            <h4 class="center">Add Feedback</h4>
            <div class="row">
              <div class="input-field col m6 s12">
                <input
                  v-model="feedback.score"
                  placeholder="Score"
                  id="feedbackScore"
                  type="number"
                  class="validate"
                />
                <label class="active" for="feedbackScore">Score</label>
              </div>
              <div class="input-field col m6 s12">
                <select v-model="feedback.project">
                  <option
                    v-for="project in projects"
                    v-bind:key="project[0]"
                    :value="project[0]"
                  >{{ project[1] }}</option>
                </select>
                <label>Project</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12">
                <textarea
                  v-model="feedback.summary"
                  placeholder="Summary"
                  id="feedbackSummary"
                  class="materialize-textarea"
                ></textarea>
                <label class="active" for="feedbackSummary">Summary</label>
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
  name: "feedback",
  props: ["studentId"],
  data() {
    return {
      feedback: {
        student: undefined,
        summary: "",
        project: "",
        score: undefined
      }
    };
  },
  async mounted() {
    $(".modal").modal();
    if (!this.$store.state.options.options.projects)
      await this.$store.dispatch("options/getOptions");
    $("select").formSelect();
  },
  computed: {
    projects() {
      return this.$store.state.options.options.projects;
    },
    feedbackList() {
      return this.$store.state.students.feedback;
    }
  },
  methods: {
    async createFeedback() {
      this.feedback.student = this.studentId;
      await this.$store.dispatch("students/createFeedback", this.feedback);
      $(".modal").modal("close");
      this.feedback = {
        student: undefined,
        summary: "",
        project: "",
        score: undefined
      };
    },
    async deleteFeedback(feedbackId) {
      await this.$store.dispatch("students/deleteFeedback", feedbackId);
    }
  }
};
</script>
