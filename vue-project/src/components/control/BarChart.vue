
<!-- Bar chart element -->
<template>
  <div id="chart">
    <apexchart type="bar" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "BarChart",
  components: {
    apexchart: VueApexCharts,
  },

  // Input array
  props: {
    numberArr: {
      type: Array,
      default: () => [0, 0, 0, 0, 0, 0],
      validator: (value) => value.every(Number.isFinite),
    },
  },

  data() {
    return {

      // Displayed array
      series: [
        {
          data: this.numberArr,
        },
      ],

      // Settings for the bar chart
      chartOptions: {
        chart: {
          type: "bar",
          height: 350,
          background: '#000',
          toolbar: {
            show: false,
          },
          animations: {
            enabled: true,
            speed: 800,
            animateGradually: {
              enabled: true,
              delay: 150
            },
            dynamicAnimation: {
              enabled: true,
              speed: 350
            }
          },
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "60%",
            borderRadius: 5,
            borderRadiusApplication: "end",
          },
        },
        dataLabels: {
          enabled: true,
          style: {
            colors: ['#fff']
          },
        },
        grid: {
          show: false,
          colors: ["#000"]
        },
        xaxis: {
          categories: [
            "pünktlich",
            "1-5 min",
            "6-15 min",
            "16-30 min",
            ">30 min",
            "Ausfall",
          ],
          labels: {
            show: true,
            hideOverlappingLabels: false,
            rotate: -45,
            rotateAlways: true,
            margin: 20,
            style: {
              colors: ['#fff', '#fff', '#fff', '#fff', '#fff', '#fff']
            },
          },
          axisBorder: {
            offsetY: 0.5,
          }
        },
        yaxis: {
          labels: {
            show: false,
            style: {
              colors: ['#fff', '#fff', '#fff', '#fff', '#fff', '#fff']
            }
          }
        },
        fill: {
          opacity: 1,
          colors: ['#474747']
        },
        tooltip: {
          theme: 'dark',
          followCursor: true,
          intersect: true,
          enabled: false,
          y: {
            formatter: function (val) {
              return val + " %";
            }
          }
        }
      }

    };
  },
};
</script>
