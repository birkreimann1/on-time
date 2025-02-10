<template>
  <div class="bg-black h-screen text-white p-8">
    <div class="flex flex-col gap-8 pb-[360px]">

      <!-- Score explanation button -->
      <div class="absolute flex justify-end right-8">
        <button class="p-2 bg-neutral-800 rounded-lg" @click="togglePopup">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" class="fill-white" height="32" width="32">
            <path
              d="M80 160c0-35.3 28.7-64 64-64l32 0c35.3 0 64 28.7 64 64l0 3.6c0 21.8-11.1 42.1-29.4 53.8l-42.2 27.1c-25.2 16.2-40.4 44.1-40.4 74l0 1.4c0 17.7 14.3 32 32 32s32-14.3 32-32l0-1.4c0-8.2 4.2-15.8 11-20.2l42.2-27.1c36.6-23.6 58.8-64.1 58.8-107.7l0-3.6c0-70.7-57.3-128-128-128l-32 0C73.3 32 16 89.3 16 160c0 17.7 14.3 32 32 32s32-14.3 32-32zm80 320a40 40 0 1 0 0-80 40 40 0 1 0 0 80z" />
          </svg>
        </button>
      </div>

      <!-- Score Circles -->
      <div class="flex justify-center items-end gap-10 pt-4">

        <!-- Enviroment based score -->
        <div class="flex flex-col items-end text-center gap-2">
          <div class="flex justify-center w-full">
            <div class="h-32 w-32 rounded-full bg-white flex justify-center items-center"
              :style="{ backgroundColor: scoreColor(scores.score) }">
              <div class="h-[120px] w-[120px] rounded-full bg-black flex justify-center items-center text-6xl">
                {{ scores.score }}
              </div>
            </div>
          </div>
          <div class="flex justify-center w-full">
            <div>Basierend auf<br />Umweltfaktoren</div>
          </div>
        </div>

        <!-- Average score -->
        <div class="flex flex-col items-center gap-2">
          <div class="h-20 w-20 rounded-full bg-white flex justify-center items-center"
            :style="{ backgroundColor: scoreColor(scores.average_score) }">
            <div class="h-[72px] w-[72px] rounded-full bg-black flex justify-center items-center text-3xl">
              {{ scores.average_score }}
            </div>
          </div>
          <div class="text-center">Allgemein</div>
        </div>
      </div>
      <div class="border-t border-neutral-500 w-full"></div>

      <!-- Bus station & line details -->
      <StationDetails :metadata="metadata" />
      <div class="border-t border-neutral-500 w-full"></div>

      <!-- Delay Information -->
      <DelayInformation :dataSizes="data_sizes" />
      <div class="border-t border-neutral-500 w-full"></div>

      <!-- BarChart -->
      <div class="justify-center text-center">
        Anteil der Verspätungstypen [%]
        <BarChart :numberArr="chartArr" />
      </div>
      <div class="border-t border-neutral-500 w-full"></div>

      <!-- Actual enviroment checkbox -->
      <div class="flex justify-between items-center">
        <div class="flex gap-4">
          <input type="checkbox" v-model="toggle" class="scale-150" @click="toggleCheckbox()" />
          <div>aktuelle Bedingungen</div>
        </div>
      </div>

      <!-- Dropdown Menus -->
      <div class="flex flex-col gap-4">
        <EnviromentDropdown :env="env" @select="handleSelection" />
      </div>
    </div>

    <!-- Score explanation Popup -->
    <ScoreExplanationPopup v-if="showPopup" @close="togglePopup" />
  </div>
</template>

<script>

// External imports
import { useRoute } from "vue-router";
import { ref, onMounted, watch, reactive } from "vue";
import { getDatabase, ref as dbRef, get as dbGet } from "firebase/database";

// Imports from project
import * as cld from "../utils/calculateLineData";
import * as translate from "../utils/stationTranslator";
import { getRawValue } from "../utils/enviromentValues";
import { getScoreColor } from '../utils/scoreColor';
import { fetchStationDataById } from '../utils/fetchDataFromFirebase';

// Components
import BarChart from "../components/control/BarChart.vue";
import StationDetails from "../components/scoreview/StationDetails.vue";
import DelayInformation from "../components/scoreview/DelayInformation.vue";
import EnviromentDropdown from "../components/scoreview/EnviromentDropdown.vue";
import ScoreExplanationPopup from "../components/scoreview/ScoreExplanationPopup.vue";

export default {
  components: {
    BarChart,
    StationDetails,
    DelayInformation,
    EnviromentDropdown,
    ScoreExplanationPopup
  },
  data() {
    return {
      showPopup: false,
    };
  },
  methods: {

    // Shows or hides popup
    togglePopup() {
      this.showPopup = !this.showPopup;
    },

    // Changes score color based on value
    scoreColor(score) {
      return getScoreColor(score);
    },

  },
  setup() {

    // Define variables
    const route = useRoute();
    const stationData = ref();
    const metadata = ref({
      name: null,
      id: null,
      line: null,
      headsign: null,
    });
    const scores = ref({
      score: null,
      average_score: null,
    });
    const line_data = ref(null);
    const data_sizes = ref({
      size: "",
      delays: "",
      incidence: "",
      average_delay: "",
      expected_delay: "",
    });
    const actual_env = reactive({
      light: "",
      temp: "",
      traffic: "",
      weather: "",
    });
    const env = reactive({
      light: "",
      temp: "",
      traffic: "",
      weather: "",
    });
    const toggle = ref(false);
    let chartArr = ref([0, 0, 0, 0, 0, 0]);

    // Executed when the view is called
    onMounted(() => {

      // Get station & line data from the page url
      if (route.query && route.query.id) {
        metadata.value.id = route.query.id;
        metadata.value.line = route.query.line;
        metadata.value.headsign = route.query.headsign;
        console.log(
          "Id:",
          metadata.value.id,
          "\nLine:",
          metadata.value.line,
          "\nHeadsign:",
          metadata.value.headsign
        );
      } else {
        console.log("No id found in route query.");
      }

      // Fetch station data from the firebase realtime database
      metadata.value.name = translate.getNameByID(metadata.value.id);
      fetchStationDataById(stationData, metadata.value.id);

    });

    // Executed when station data is fetched from firebase
    watch(
      () => stationData.value,
      (newValue) => {
        if (newValue && Object.keys(newValue).length > 0) {

          // Stores line data
          line_data.value = stationData.value.lines[metadata.value.line];

          // Stores enviroment data
          const env_data = stationData.value.env_data;
          for (const key in env_data) {
            env[key] = env_data[key];
            actual_env[key] = env_data[key];
          }

          // Set checkbox true
          toggle.value = true

          // Generate average score
          scores.value.average_score = cld.calculateAverageScore(
            line_data.value.light
          );

          // All enviroment dependent displays and values are updated
          updateScoresAndChart();

        }
      }
    );

    // Executed when a enviroment value is changed via dropdown menu
    const handleSelection = (category, selectedValue) => {

      // Updates changed enviroment value
      env[category] = [getRawValue(selectedValue, category)];
      console.log(`Selected ${category}:`, selectedValue);

      // Updates all enviroment dependent displays and values
      updateScoresAndChart();

      // Checks if set enviroment values are equal to the actual enviroment
      // If equal sets the checkbox to true
      if (JSON.stringify(env) === JSON.stringify(actual_env)) {
        toggle.value = true;
      } else {
        toggle.value = false;
      }

    };

    // Updates all enviroment dependent displays and values
    const updateScoresAndChart = () => {
      scores.value.score = cld.calculateScore(line_data.value, env);
      data_sizes.value = cld.calculateDelayData(line_data.value, env);
      chartArr.value.splice(
        0,
        6,
        ...cld.fillChartArr(line_data.value, data_sizes.value, env)
      );
    };

    // When checkbox is set to true overwrites used enviroment data with the actual values
    const toggleCheckbox = () => {
      if (!toggle.value) {
        for (const key in env) {
          env[key] = actual_env[key];
        }

        // Updates all enviroment dependent displays and values
        updateScoresAndChart();

      }
    };

    return {
      stationData,
      metadata,
      scores,
      data_sizes,
      env,
      actual_env,
      toggle,
      chartArr,
      handleSelection,
      toggleCheckbox
    };
  },
};
</script>