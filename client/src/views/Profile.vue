<template>
  <div class="container" v-if="mentor">
    <h4>
      {{ mentor.fullname }}
      <a href="#" @click="showEditForm">
        <i class="fas fa-pencil-alt"></i>
      </a>
      &nbsp;
      <a id="logOutBtn" class="btn" href="#" @click="logout">Logout</a>
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
            />
            <label class="active" for="mentorName">Name</label>
          </div>
          <div class="input-field col s12">
            <input
              v-model="mentor.address"
              placeholder="e.g 9756 Vernon Drive"
              id="mentorAddress"
              type="text"
            />
            <label class="active" for="mentorAddress">Address Line 1</label>
          </div>
          <div class="input-field col s12">
            <input v-model="mentor.address_more" placeholder id="mentorAddress2" type="text" />
            <label class="active" for="mentorAddress2">Address Line 2</label>
          </div>
          <div class="input-field col s12">
            <input
              v-model="mentor.city_country"
              placeholder="e.g Paris, France"
              id="mentorCity"
              type="text"
            />
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

    <hr />

    <div>
      <div class="input-field">
        <select class="browser-default" v-model="month" @change="createCharts">
          <option
            v-for="month in availableMonths"
            v-bind:key="month"
            :value="month"
          >Month: {{ month }}</option>
        </select>
      </div>
      <span class="right">
        Invoice
        <button class="btn" @click="showInvoiceForm = !showInvoiceForm">
          <i class="fas fa-money-check"></i>
        </button>
      </span>
      <div v-show="showInvoiceForm" class="row">
        <form class="col s12" @submit.prevent="generateInvoice">
          <div class="row">
            <div class="input-field col m6 s12">
              <input
                v-model="invoice.date"
                placeholder="Date"
                id="invoiceDate"
                type="date"
                class="validate"
              />
              <label class="active" for="invoiceDate">Date</label>
            </div>
            <div class="input-field col m6 s12">
              <input v-model="invoice.number" id="invoiceNumber" type="text" />
              <label class="active" for="invoiceNumber">Invoice Number</label>
            </div>
            <div class="input-field col m6 s12">
              <input v-model="invoice.hourlyFee" id="hourlyFee" type="text" />
              <label class="active" for="hourlyFee">Hourly Fee</label>
            </div>
          </div>
          <button class="btn">Generate Invoice</button>
        </form>
      </div>

      <p>Hours: {{ totals.hours }}</p>
      <p>Total Billable: &euro;{{ totals.euros_billable }}</p>
    </div>

    <div id="dayVsMins"></div>
  </div>
</template>



<script>
import moment from "moment";
import axios from "../_config";

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
      showInvoiceForm: false,
      mentor: this.$store.state.authentication.user,
      monthDim: "",
      invoice: {
        date: this.getInvoiceNumberDate(),
        number: this.getInvoiceNumberDate("number"),
        hourlyFee: 50
      }
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
      self.monthDim = "";
    },
    showEditForm() {
      this.editMentorDetail = !this.editMentorDetail;
    },
    getLastDay() {
      let year, month;
      if (!this.month) {
        const today = new Date();
        year = today.getFullYear();
        month = today.getMonth();
      } else {
        [year, month] = this.month.split("-");
      }
      return new Date(Number(year), Number(month), 0);
    },
    getInvoiceNumberDate(type) {
      const date = this.getLastDay();
      return type == "number"
        ? moment(+date).format("#YYYYMM")
        : moment(+date).format("YYYY-MM-DD");
    },
    async updateMentorDetails() {
      await this.$store.dispatch("authentication/updateMentor", this.mentor);
      this.editMentorDetail = false;
    },
    async generateInvoice() {
      const res = await axios.post(`mentors/invoice/`, this.invoice);
      alert(
        `Invoice PDF sent to your inbox(${this.$store.state.authentication.user.email})`,
        "success"
      );
      this.showInvoiceForm = false;
    },
    createCharts() {
      this.invoice.number = this.getInvoiceNumberDate("number");
      this.invoice.date = this.getInvoiceNumberDate();
      const data = this.logData;
      let facts = crossfilter(data);
      let all = facts.groupAll();

      this.monthDim = facts.dimension(d => d.month);
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
        .range(this.getLastDay().getDate())
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
        .x(d3.scaleBand().domain(xAxisDomain))
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
        euros_billable: String((hours * this.billRate).toFixed(3)).slice(0, -1)
      };
    },
    logout() {
      this.$store.dispatch("authentication/logout");
      this.$store.dispatch("clearAll");
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