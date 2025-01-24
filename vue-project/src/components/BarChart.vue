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
      default: () => [0, 0, 0, 0, 0, 0], // Important: Use a factory function for default array values
      validator: (value) => {
        console.log(value)
        return value.every(Number.isFinite); // Check if all elements are numbers
      },
    },
    chartTitle: {
      type: String,
      default: "Anteil der Verspätungstypen [%]",
      show: true,
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
          dropShadow: {
            enabled: true,
            enabledOnSeries: undefined,
            top: 0,
            left: 0,
            blur: 6,
            color: '#ff0000',
            opacity: .35
          }
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "65%",
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
          borderColor: '#777',
        },
        stroke: {
          show: true,
          width: 2,
          colors: ['#bbb']
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
            style: {
              colors: ['#fff', '#fff', '#fff', '#fff', '#fff', '#fff',]
            },
          }
        },
        yaxis: {
              labels: {
            show: false,
            style: {
              colors: ['#fff', '#fff', '#fff', '#fff', '#fff', '#fff',]
            }
          }
          
        },
        fill: {
          opacity: 1,
          colors: ['#222']
        },
        tooltip: {
          theme: 'dark',
          followCursor: true,
          intersect: true,
          y: {
            formatter: function (val) {
              return val + " %"
            }
          }
        }  
      } 
    };
  },
};
</script>
