<template>
  <div class="container">
    <div v-if="student && mentor">
      <h4 class="center">
        Log Session with
        <router-link :to="{ name: 'student-detail', params: { id: student.id } }">{{ student.name }}</router-link>
      </h4>
      <div class="row">
        <form class="col s12" @submit.prevent="createLog">
          <div class="row">
            <div class="input-field col m6 s12">
              <input type="date" id="date" v-model="log.date" required />
              <label class="active" for="date">Date</label>
            </div>

            <div class="input-field col m2 s4">
              <input type="number" v-model="hours" min="0" max="99" id="hours" required />
              <label class="active" for="hours">(hours)</label>
            </div>
            <div class="input-field col m2 s4">
              <input type="number" v-model="minutes" min="0" max="60" id="mins" required />
              <label class="active" for="mins">(minutes)</label>
            </div>
            <div class="input-field col m2 s4">
              <input type="number" v-model="seconds" min="0" max="60" id="secs" required />
              <label class="active" for="secs">(seconds)</label>
            </div>
          </div>
          <div class="row">
            <div class="input-field col m6 s12">
              <select v-model="sessionType" multiple>
                <option
                  v-for="stype in sessionTypes"
                  v-bind:key="stype[0]"
                  :value="stype[0]"
                >{{ stype[1] }}</option>
              </select>
              <label>Session Type</label>
            </div>
            <div class="input-field col m6 s12">
              <select v-model="log.projects" multiple>
                <option v-for="proj in projects" v-bind:key="proj[0]" :value="proj[0]">{{ proj[1] }}</option>
              </select>
              <label>Project Covered</label>
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
          <div class="right">
            <a @click="toggleShowMore" class="btn-small">
              {{
              showMore ? "Less..." : "More..."
              }}
            </a>
          </div>

          <div class="log-buttons">
            <div class="switch">
              <label>
                Fill Google Form on Submit
                <a target="_blank" :href="logUrl">(Preview Google Form.)</a>
                <input type="checkbox" @change="fillGoogleForm" />
                <span class="lever"></span>
              </label>
            </div>

            <button @click.prevent="deleteLog" v-show="this.$route.params.logid" class="btn red">Del</button>
            <button class="btn">Submit</button>
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
        date: undefined,
        duration: "",
        types: "",
        concern: "",
        projects: [],
        summary: "",
        feeling: "average"
      },
      hours: undefined,
      minutes: undefined,
      seconds: undefined,
      sessionType: [],
      showMore: false,
      runE2E: false,
      projects: this.$store.state.options.options.projects
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
    logUrl() {
      const options = this.$store.state.options.options;
      const rootUrl = options.formUrl,
        mentorEmail = `&emailAddress=${this.mentor.email}`,
        mentorName = `&entry.838873576=${this.mentor.fullname}`,
        date = `&entry.1191000917=${this.log.date}`,
        studentEmail = `&entry.1269347964=${this.student.email}`,
        types = this.sessionType.reduce(
          (cummulative, item) =>
            cummulative + `&entry.1521715512=${options.typeDict[item]}`,
          ""
        ),
        projects = this.log.projects.reduce(
          (cummulative, item) =>
            cummulative + `&entry.478142644=${options.projectDict[item]}`,
          ""
        ),
        duration = `&entry.775489883=${this.formatTime(":")}`,
        feeeling = `&entry.2010663110=${options.feelingDict[this.log.feeling]}`,
        summary = `&entry.1882714143=${this.log.summary}`,
        concern = `&entry.401267824=${this.log.concern}&emailReceipt=true`;

      return encodeURI(
        rootUrl +
          mentorEmail +
          mentorName +
          date +
          studentEmail +
          types +
          projects +
          duration +
          feeeling +
          summary +
          concern
      );
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
    formatTime(seperator = "-") {
      const result = [];
      for (let num of [this.hours, this.minutes, this.seconds]) {
        num = num ? String(num) : "00";
        if (num.length <= 1) num = "0" + num;
        result.push(num);
      }
      return result.join(seperator);
    },
    async createLog() {
      const log = {
        student: this.student.id,
        mentor: this.mentor.id,
        date: this.log.date,
        duration: this.formatTime(),
        types: this.sessionType.join("|"),
        concern: this.log.concern,
        projects: JSON.stringify(this.log.projects),
        summary: this.log.summary,
        feeling: this.log.feeling
      };

      let newLog;
      if (this.$route.params.logid) {
        const res = await this.$store.dispatch("logs/updateLog", log);
        newLog = res.data;
      } else {
        newLog = await this.$store.dispatch("logs/createLog", log);
      }
      if (this.runE2E) {
        window.open(this.logUrl);
      }
      router.push("/sessions");
    },
    deleteLog() {
      const confirmDelete = confirm("Sure?");
      if (confirmDelete) this.$store.dispatch("logs/deleteLog", this.log);
    }
  }
};
</script>

<style>
.log-buttons .btn:first-child {
  margin-right: 20px;
}
.switch {
  margin: 15px 0;
}
</style>

