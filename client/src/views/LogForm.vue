<template>
  <div class="container">
    <div v-if="student && mentor">
      <h4 class="center">Log Session with {{ student.name }}</h4>
      <div class="row">
        <form class="col s12" @submit.prevent="createLog">
          <div class="row">
            <div class="input-field col m6 s12">
              <input type="date" id="date" v-model="log.date" required>
              <label class="active" for="date">Date</label>
            </div>

            <div class="input-field col m2 s4">
              <input type="number" v-model="hours" min="0" max="99" id="hours" required>
              <label class="active" for="hours">(hours)</label>
            </div>
            <div class="input-field col m2 s4">
              <input type="number" v-model="minutes" min="0" max="60" id="mins" required>
              <label class="active" for="mins">(minutes)</label>
            </div>
            <div class="input-field col m2 s4">
              <input type="number" v-model="seconds" min="0" max="60" id="secs" required>
              <label class="active" for="secs">(seconds)</label>
            </div>
          </div>
          <div class="row">
            <div class="input-field col s12">
              <select v-model="sessionType" multiple>
                <option
                  v-for="stype in sessionTypes"
                  v-bind:key="stype[0]"
                  :value="stype[0]"
                >{{ stype[1] }}</option>
              </select>
              <label>Session Type</label>
            </div>
          </div>
          <div class="row">
            <div class="input-field col s12">
              <textarea id="summary" v-model="log.summary" class="materialize-textarea" required></textarea>
              <label for="summary">Summary</label>
            </div>
          </div>
          <div class="row">
            <div class="input-field col s12">
              <select v-model="log.feeling">
                <option
                  v-for="feeling in feelings"
                  v-bind:key="feeling[0]"
                  :value="feeling[0]"
                >{{ feeling[1] }}</option>
              </select>
              <label>
                What is your general feeling on the student's progress so
                far?
              </label>
            </div>
          </div>
          <div v-show="showMore" class="more-options">
            <div class="row">
              <div class="input-field col s12">
                <textarea id="concern" v-model="log.concern" class="materialize-textarea"></textarea>
                <label for="concern">
                  Are there any issues that you'd like Student Care to help
                  address?
                </label>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="switch">
              <label class="right">
                Fill Google Form
                <a target="_blank" href="https://github.com/tonymontaro/logger-mentorci">info</a>
                <input type="checkbox" @change="fillGoogleForm">
                <span class="lever"></span>
              </label>
            </div>
            <a @click="toggleShowMore" class="btn-small">
              {{
              showMore ? "Less..." : "More..."
              }}
            </a>
          </div>

          <div class="log-buttons right">
            <button @click.prevent="deleteLog" v-show="this.$route.params.logid" class="btn red">Del</button>
            <button class="btn">Save</button>
          </div>
        </form>
      </div>
    </div>
    <div v-else>
      <h4>No student with specified ID found or not logged in.</h4>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import { runGoogleFormProcess } from "../_helpers";
import router from "../router";

export default {
  name: "student-detail",
  data() {
    return {
      log: {
        student: 0,
        mentor: 0,
        date: moment().format("YYYY-MM-DD"),
        duration: "",
        types: "",
        concern: "",
        summary: "",
        feeling: "average"
      },
      hours: 0,
      minutes: 0,
      seconds: 0,
      sessionType: [],
      showMore: false,
      runE2E: false
    };
  },
  mounted() {
    if (this.$route.params.logid) {
      const log = this.$store.state.logs.logs.filter(
        lg => lg.id == this.$route.params.logid
      )[0];
      if (log) {
        const [hours, minutes, seconds] = log.duration
          .split("-")
          .map(i => Number(i));
        this.log = log;
        this.hours = hours;
        this.minutes = minutes;
        this.seconds = seconds;
        this.sessionType = log.types.split("|");
      } else {
        router.push("/");
      }
    }
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
    mentor() {
      return this.$store.state.authentication.user;
    },
    sessionTypes() {
      return this.$store.state.logs.sessionTypes;
    },
    feelings() {
      return this.$store.state.logs.sessionFeelings;
    }
  },
  methods: {
    fillGoogleForm(e) {
      this.runE2E = e.target.checked;
    },
    toggleShowMore() {
      this.showMore = !this.showMore;
    },
    formatTime() {
      const result = [];
      for (let num of [this.hours, this.minutes, this.seconds]) {
        num = num ? String(num) : "00";
        if (num.length <= 1) num = "0" + num;
        result.push(num);
      }
      return result.join("-");
    },
    async createLog() {
      this.log.types = this.sessionType.join("|");
      this.log.student = this.student.id;
      this.log.mentor = this.mentor.id;
      this.log.duration = this.formatTime();
      if (this.$route.params.logid) {
        await this.$store.dispatch("logs/updateLog", this.log);
      } else {
        const newLog = await this.$store.dispatch("logs/createLog", this.log);
        if (this.runE2E) {
          runGoogleFormProcess(newLog.id);
        }
      }
    },
    deleteLog() {
      this.$store.dispatch("logs/deleteLog", this.log);
    }
  }
};
</script>

<style>
.log-buttons .btn:first-child {
  margin-right: 20px;
}
</style>

