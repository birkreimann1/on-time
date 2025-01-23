<template>
  <div id="chart">
    <apexchart
      type="bar"
      height="350"
      :options="chartOptions"
      :series="series"
    ></apexchart>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "BarChart",
  components: {
    apexchart: VueApexCharts,
  },
  props: {
    numberArr: {
      type: Array,
      default: () => [], // Important: Use a factory function for default array values
      validator: (value) => {
        return value.every(Number.isFinite); // Check if all elements are numbers
      },
    },
    chartTitle: {
      type: String,
      default: "Anzahl",
    },
  },
  data() {
    return {
      series: [
        {
          data: this.numberArr,
        },
      ],
      chartOptions: {
        chart: {
          type: "bar",
          height: 350,
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "55%",
            borderRadius: 5,
            borderRadiusApplication: "end",
          },
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          show: true,
          width: 2,
          colors: ["transparent"],
        },
        xaxis: {
          categories: [
            "no delay",
            "short",
            "medium",
            "long",
            "extreme",
            "cancelled",
          ],
        },
        yaxis: {
          title: {
            text: "Anzahl",
          },
        },
        fill: {
          opacity: 1,
        },
      },
    };
  },
};
</script>
