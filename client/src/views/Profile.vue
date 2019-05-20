<template>
  <div class="container" v-if="mentor">
    <h4>
      {{ mentor.fullname }}
      <a href="#" @click="showEditForm">
        <i class="fas fa-pencil-alt"></i>
      </a>
    </h4>
    <div v-show="!editMentorDetail">
      <p>Email: {{ mentor.email }}</p>
    </div>

    <div v-show="editMentorDetail" class="row">
      <form class="col s12" @submit.prevent="updateMentorDetails">
        <div class="row">
          <div class="input-field col s12">
            <input
              v-model="mentor.fullname"
              placeholder="Name"
              id="mentorName"
              type="text"
              class="validate"
            >
            <label class="active" for="mentorName">Name</label>
          </div>
          <div class="input-field col s12">
            <input
              v-model="mentor.address"
              placeholder="e.g 9756 Vernon Drive"
              id="mentorAddress"
              type="text"
            >
            <label class="active" for="mentorAddress">Address Line 1</label>
          </div>
          <div class="input-field col s12">
            <input v-model="mentor.address_more" placeholder id="mentorAddress2" type="text">
            <label class="active" for="mentorAddress2">Address Line 2</label>
          </div>
          <div class="input-field col s12">
            <input
              v-model="mentor.city_country"
              placeholder="e.g Paris, France"
              id="mentorCity"
              type="text"
            >
            <label class="active" for="mentorCity">City/Province, Country</label>
          </div>
          <div class="input-field col s12">
            <textarea
              v-model="mentor.bio"
              placeholder="Bio"
              id="mentorBio"
              class="materialize-textarea"
            ></textarea>
            <label class="active" for="mentorBio">Bio</label>
          </div>
        </div>
        <button class="btn">Save</button>
      </form>
    </div>

    <hr>

    <div>
      <div class="row">
        <div class="input-field col m6 s12">
          <select v-model="month" @change="createCharts">
            <option v-for="month in availableMonths" v-bind:key="month" :value="month">{{ month }}</option>
          </select>
          <label>Month</label>
        </div>
      </div>
      <p>Hours: {{ totals.hours }}</p>
      <p>Total Billable: &euro;{{ totals.euros_billable }}</p>
    </div>

    <div id="dayVsMins"></div>
  </div>
</template>



<script>
export default {
  name: "logs",
  data() {
    return {
      totals: {
        mins: 0,
        hours: 0,
        euros_billable: 0
      },
      billRate: 50,
      month: this.getCurrentYearMonth(),
      editMentorDetail: false,
      mentor: this.$store.state.authentication.user,
      monthDim: ""
    };
  },
  mounted() {
    this.fetchLogs();
  },
  computed: {
    logData() {
      return this.$store.state.logs.logs.map(log => {
        return {
          id: log.id,
          date: log.date,
          month: log.date.slice(0, 7),
          fullDate: new Date(log.date),
          duration: log.durationInMins
        };
      });
    },
    availableMonths() {
      const months = [];
      this.logData.map(d => {
        const year = d.fullDate.getFullYear();
        let month = d.fullDate.getMonth() + 1;
        month = month > 8 ? month : "0" + month;
        const date = `${year}-${month}`;
        if (!months.includes(date)) months.push(date);
      });
      this.month = months[0];
      return months;
    }
  },
  methods: {
    async fetchLogs() {
      if (this.$store.state.logs.logs.length === 0) {
        await this.$store.dispatch("logs/getLogs");
      }
      this.createCharts();
      $("select").formSelect();
      self.monthDim = "";
    },
    showEditForm() {
      this.editMentorDetail = !this.editMentorDetail;
    },
    async updateMentorDetails() {
      await this.$store.dispatch("authentication/updateMentor", this.mentor);
      this.editMentorDetail = false;
    },
    createCharts() {
      if (this.monthDim) {
        this.monthDim.filter(this.month);
        dc.redrawAll();
      } else {
        const data = this.logData;
        let facts = crossfilter(data);
        let all = facts.groupAll();

        const allDim = facts.dimension(d => d.date);
        this.monthDim = facts.dimension(d => d.month);
        var yAxis = d3
          .scaleLinear()
          .domain([
            0,
            allDim
              .group()
              .reduceSum(d => d.duration)
              .top(1)[0].value
          ])
          .range([0, 960]);
        this.monthDim.filter(this.month);

        const display = () => {
          this.setTotals(
            facts
              .groupAll()
              .reduceSum(d => d.duration)
              .value()
          );
        };
        const xAxisDomain = d3
          .range(31)
          .map(i => `${i > 8 ? i + 1 : "0" + (i + 1)}`);
        const dayDim = facts.dimension(d => d.date.slice(-2));
        const dayGroup = dayDim.group().reduceSum(d => d.duration);

        dc.barChart("#dayVsMins")
          .width(500)
          .height(300)
          .margins({ top: 10, right: 50, bottom: 40, left: 30 })
          .dimension(dayDim)
          .group(dayGroup)
          .on("pretransition", display)
          .yAxisLabel("Time (mins)")
          .xAxisLabel("Day")
          .y(yAxis)
          .x(d3.scaleBand().domain(xAxisDomain))
          .xUnits(dc.units.ordinal);

        dc.renderAll();
      }
    },
    getCurrentYearMonth() {
      const today = new Date();
      let currentMonth = String(today.getMonth() + 1);
      currentMonth =
        currentMonth.length == 2 ? currentMonth : "0" + currentMonth;
      return `${today.getFullYear()}-${currentMonth}`;
    },
    setTotals(mins) {
      const hours = mins / 60;
      this.totals = {
        mins: mins,
        hours: hours.toFixed(2),
        euros_billable: (hours * this.billRate).toFixed(2)
      };
    }
  }
};
</script>

<style>
div.dc-chart {
  float: none;
}

#dayVsMins .x.axis text {
  text-anchor: end !important;
  transform: rotate(-45deg) translate(-5px, -5px);
}
</style>