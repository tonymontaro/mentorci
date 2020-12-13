<template>
  <div class="container">
    <div class="input-field">
      <input type="text" placeholder="Search..." v-model="search" />
    </div>

    <div class="row" v-if="logs.length > 0 && Object.keys(studentsMap).length > 0">
      <div class="col s12" v-for="log in pageOfItems" v-bind:key="log.id">
        <div v-if="log.student" class="card blue-grey darken-1 log-card">
          <div href="#" class="card-content white-text">
            <router-link
              :to="{ name: 'log-edit-form', params: { id: log.student, logid: log.id } }"
            >
              <span class="card-title">{{ log.id }} | Date: {{ log.date }}</span>
            </router-link>

            <p>
              <span class="yellow-text">Name:</span>
              {{studentsMap[log.student].name}} |
              <span class="yellow-text">Duration:</span>
              {{ parseInt(log.durationInMins) }}mins |
              <span class="yellow-text">Type:</span>
              {{log.types.split('|').join(', ')}} |
              <span
                class="yellow-text"
              >Project(s):</span>
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

          <div class="card-footer pb-0 pt-3">
            <jw-pagination :items="logs" @changePage="onChangePage" :disableDefaultStyles="true"></jw-pagination>
        </div>

    <div class="fixed-action-btn">
      <a class="btn-floating btn-large" href="#pageTop">
        <i class="fas fa-chevron-up"></i>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "logs",
  data() {
    return {
      search: "",
      pageOfItems: []
    };
  },
  computed: {
    logs() {
      let result = this.$store.state.logs.logs;
      if (!this.search) return result;
      result = result.filter(log => {
        const searchTerm = this.search.toLowerCase();
        return (
          log.summary.toLowerCase().includes(searchTerm) ||
          log.concern.toLowerCase().includes(searchTerm)
        );
      });
      return result;
    },
    studentsMap() {
      let students = this.$store.state.students.students;
      const sMap = {};
      for (let student of students) {
        sMap[student.id] = student;
      }
      return sMap;
    }
  },
  mounted() {
    $("select").formSelect();
    this.fetchLogs();
  },
  methods: {
    async fetchLogs() {
      if (this.$store.state.logs.logs.length === 0) {
        await this.$store.dispatch("logs/getLogs");
      }
    },
    onChangePage(pageOfItems) {
      this.pageOfItems = pageOfItems;
    }
  }
};
</script>

<style>
.log-card .card-content {
  padding: 10px 20px;
}

</style>
