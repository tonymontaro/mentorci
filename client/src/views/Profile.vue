<template>
  <div class="container" v-if="this.$store.state.authentication.user">
    <h4>{{ this.$store.state.authentication.user.fullname }}</h4>
    <p>Email: {{ this.$store.state.authentication.user.email }}</p>

    <hr>

    <div>
      <h5>Month: {{ this.month }}</h5>
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
      month: ""
    };
  },
  mounted() {
    this.fetchLogs();
  },
  computed: {
    logs() {
      let result = this.$store.state.logs.logs;
    }
  },
  methods: {
    async fetchLogs() {
      if (this.$store.state.logs.logs.length === 0) {
        await this.$store.dispatch("logs/getLogs");
      }
      this.createCharts();
    },
    createCharts() {
      const data = this.$store.state.logs.logs.map(log => {
        return {
          id: log.id,
          date: log.date,
          month: log.date.slice(0, 7),
          fullDate: new Date(log.date),
          duration: log.durationInMins
        };
      });
      let facts = crossfilter(data);
      let all = facts.groupAll();

      const currentYearMonth = this.getCurrentYearMonth();
      let monthDim = facts.dimension(d => d.month);
      this.month = currentYearMonth;
      monthDim.filter(currentYearMonth);

      const display = () => {
        this.setTotals(
          facts
            .groupAll()
            .reduceSum(d => d.duration)
            .value()
        );
      };
      const dateSet = [];
      const dayDim = facts.dimension(d => {
        if (dateSet.indexOf(d.date) == -1) {
          dateSet.push(d.date);
        }
        return d.date;
      });
      const dayGroup = dayDim.group().reduceSum(d => d.duration);
      dc.barChart("#dayVsMins")
        .width(500)
        .height(300)
        .margins({ top: 10, right: 50, bottom: 70, left: 30 })
        .dimension(dayDim)
        .group(dayGroup)
        .on("pretransition", display)
        .yAxisLabel("Time (mins)")
        .xAxisLabel("Day")
        .x(d3.scaleBand().domain(dateSet.reverse()))
        .xUnits(dc.units.ordinal);

      dc.renderAll();
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
  transform: rotate(-45deg);
}
</style>