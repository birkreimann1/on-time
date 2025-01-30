<template>
  <div class="bg-black h-screen text-white p-8">
    <!-- Main Content -->
    <div class="flex flex-col gap-8 pb-[360px]">
      <!-- Optional Back Button
      <div class="absolute left-8 top-8">
        <button class="p-2 rounded-lg" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" class="fill-white" height="32" width="32">
            <path
              d="M44.5 238.5L178.3 94.7c9.3-9.3 24.6-9.3 33.9 0l25.4 25.4c9.3 9.3 9.3 24.6 0 33.9L139.5 256l98.1 98.1c9.3 9.3 9.3 24.6 0 33.9l-25.4 25.4c-9.3 9.3-24.6 9.3-33.9 0L44.5 238.5c-9.3-9.3-9.3-24.6 0-33.9z" />
          </svg>
        </button>
      </div>
      -->

      <!-- Question Mark Button -->
      <div class="absolute flex justify-end right-8">
        <button class="p-2 bg-neutral-800 rounded-lg" @click="togglePopup">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 320 512"
            class="fill-white"
            height="32"
            width="32"
          >
            <path
              d="M80 160c0-35.3 28.7-64 64-64l32 0c35.3 0 64 28.7 64 64l0 3.6c0 21.8-11.1 42.1-29.4 53.8l-42.2 27.1c-25.2 16.2-40.4 44.1-40.4 74l0 1.4c0 17.7 14.3 32 32 32s32-14.3 32-32l0-1.4c0-8.2 4.2-15.8 11-20.2l42.2-27.1c36.6-23.6 58.8-64.1 58.8-107.7l0-3.6c0-70.7-57.3-128-128-128l-32 0C73.3 32 16 89.3 16 160c0 17.7 14.3 32 32 32s32-14.3 32-32zm80 320a40 40 0 1 0 0-80 40 40 0 1 0 0 80z"
            />
          </svg>
        </button>
      </div>

      <!-- Score Circles -->
      <div class="flex justify-center items-end gap-10 pt-4">
        <div class="flex flex-col items-end text-center gap-2">
          <div class="flex justify-center w-full">
            <div
              class="h-32 w-32 rounded-full bg-white flex justify-center items-center"
              :style="{ backgroundColor: getScoreColor(scores.score) }"
            >
              <div
                class="h-[120px] w-[120px] rounded-full bg-black flex justify-center items-center text-6xl"
              >
                {{ scores.score }}
              </div>
            </div>
          </div>
          <div class="flex justify-center w-full">
            <div>Basierend auf<br />Umweltfaktoren</div>
          </div>
        </div>
        <div class="flex flex-col items-center gap-2">
          <div
            class="h-20 w-20 rounded-full bg-white flex justify-center items-center"
            :style="{ backgroundColor: getScoreColor(scores.average_score) }"
          >
            <div
              class="h-[72px] w-[72px] rounded-full bg-black flex justify-center items-center text-3xl"
            >
              {{ scores.average_score }}
            </div>
          </div>
          <div class="text-center">Allgemein</div>
        </div>
      </div>

      <!-- Bus Station Info -->
      <div class="flex flex-col gap-4">
        <div class="border-t border-neutral-500 w-full"></div>
        <div
          class="flex flex-col items-center gap-1 font-bold text-white text-center"
        >
          <div
            class="text-3xl font-extrabold bg-clip-text text-neutral-100 mb-3"
          >
            {{ metadata.name }}
          </div>
          <div
            class="text-2xl font-bold text-white mb-1 bg-neutral-800 px-4 py-2 rounded-lg inline-block"
          >
            {{ metadata.line }}
          </div>
          <div class="text-lg text-neutral-200 italic">
            {{ metadata.headsign }}
          </div>
        </div>
        <div class="border-t border-neutral-500 w-full"></div>
      </div>

      <!-- Additional Information -->
      <div class="flex flex-col gap-8">
        <div class="flex justify-center gap-4">
          <div class="flex flex-col gap-4 items-starts">
            <div>Einbezogene Fahrten</div>
            <div>davon Verspätungen</div>
            <div>Verspätungsrate</div>
            <div>Verspätung (Ø)</div>
            <div>Erwartete Verspätung</div>
          </div>
          <div class="border-l border-gray-300"></div>
          <div class="flex flex-col gap-4">
            <div>{{ data_sizes.size || "0" }}</div>
            <div>{{ data_sizes.delays || "0" }}</div>
            <div>{{ data_sizes.incidence || "N/A" }}</div>
            <div>{{ data_sizes.average_delay }}</div>
            <div>{{ data_sizes.expected_delay }}</div>
          </div>
        </div>
      </div>

      <div class="border-t border-neutral-500 w-full"></div>

      <!-- BarChart -->
      <div class="justify-center text-center">
        Anteil der Verspätungstypen [%]
        <BarChart :numberArr="chartArr" />
        <div class="border-t border-neutral-500 w-full"></div>
      </div>

      <div class="flex flex-col gap-6">
        <!-- Checkbox -->
        <div class="flex justify-between items-center">
          <div class="flex gap-4">
            <input
              type="checkbox"
              v-model="toggle"
              class="scale-150"
              @click="toggleCheckbox()"
            />
            <div>aktuelle Bedingungen</div>
          </div>
        </div>

        <!-- Dropdown -->
        <div class="flex flex-col gap-4">
          <div class="flex flex-col gap-1">
            <p>Lichtverhältnisse</p>
            <Dropdown
              :actualEnv="env.light"
              label="light"
              @select="handleSelection('light', $event)"
            />
          </div>
          <div class="flex flex-col gap-1">
            <p>Temperatur</p>
            <Dropdown
              :actualEnv="env.temp"
              label="temp"
              @select="handleSelection('temp', $event)"
            />
          </div>
          <div class="flex flex-col gap-1">
            <p>Verkehr</p>
            <Dropdown
              :actualEnv="env.traffic"
              label="traffic"
              @select="handleSelection('traffic', $event)"
            />
          </div>
          <div class="flex flex-col gap-1">
            <p>Wetter</p>
            <Dropdown
              :actualEnv="env.weather"
              label="weather"
              @select="handleSelection('weather', $event)"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Popup -->
    <div v-if="showPopup" class="fixed inset-0 bg-black bg-opacity-50">
      <div
        class="bg-neutral-800 text-neutral-200 p-8 rounded-lg shadow-lg w-full"
      >
        <div class="flex justify-between">
          <h2 class="text-xl font-bold">
            Wie setzten sich die Scores zusammen?
          </h2>
          <div>
            <button
              @click="togglePopup"
              class="p-1 bg-neutral-900 rounded-lg flex-grow-0"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 384 512"
                class="fill-white"
                height="32"
                width="32"
              >
                <path
                  d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"
                />
              </svg>
            </button>
          </div>
        </div>
        <ScoreExplanation />
      </div>
    </div>
  </div>
</template>

<script>
import Dropdown from "../components/Dropdown.vue";
import { useRoute } from "vue-router";
import { ref, onMounted, watch, reactive } from "vue";
import { getDatabase, ref as dbRef, get as dbGet } from "firebase/database";
import * as cld from "../utils/calculateLineData";
import * as translate from "../utils/stationTranslator";
import { getRawValue } from "../utils/enviromentValues";
import ScoreExplanation from "../components/ScoreExplanation.vue";
import BarChart from "../components/BarChart.vue";

export default {
  components: {
    Dropdown,
    ScoreExplanation,
    BarChart,
  },
  data() {
    return {
      showPopup: false,
    };
  },
  computed: {
    scoreColor() {
      return this.getScoreColor(this.item.score);
    },
  },
  methods: {
    togglePopup() {
      this.showPopup = !this.showPopup;
    },
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },
    goBack() {
      this.$router.back();
    },
    getScoreColor(score) {
      if (score >= 90) {
        return "#397d3b";
      } else if (score >= 75) {
        return "#d9ad1e";
      } else if (score >= 50) {
        return "#b3721d";
      } else if (score >= 1) {
        return "#8f2c25";
      } else {
        return "##ffffff";
      }
    },
    handleSelection(category, selectedValue) {
      this.env[category] = [getRawValue(selectedValue, category)];

      console.log(`Selected ${category}:`, selectedValue);
      this.scores.score = cld.calculateScore(this.line_data, this.env);
      this.data_sizes = cld.calculateDelays(this.line_data, this.env);
      this.chartArr.splice(
        0,
        6,
        ...cld.fillChartArrNew(this.line_data, this.data_sizes, this.env)
      );

      if (JSON.stringify(this.env) === JSON.stringify(this.actual_env)) {
        this.toggle = true;
      } else {
        this.toggle = false;
      }
    },
    toggleCheckbox() {
      if (!this.toggle) {
        this.env = { ...this.actual_env };
        this.scores.score = cld.calculateScore(this.line_data, this.env);
        this.data_sizes = cld.calculateDelays(this.line_data, this.env);
        this.chartArr.splice(
          0,
          6,
          ...cld.fillChartArrNew(this.line_data, this.data_sizes, this.env)
        );
      }
    },
  },
  setup() {
    const route = useRoute();
    const startMessage = ref("");
    const stationData = ref([]);
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

    const fetchStations = async () => {
      const db = getDatabase();
      const stationsRef = dbRef(
        db,
        `stations_new_score/${String(metadata.value.id)}`
      );

      try {
        const snapshot = await dbGet(stationsRef);
        if (snapshot.exists()) {
          stationData.value = snapshot.val();
        } else {
          console.log("No data available");
        }
      } catch (error) {
        console.error("Error fetching data from Firebase:", error);
      }
    };

    onMounted(() => {
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

      metadata.value.name = translate.getNameByID(metadata.value.id);
      fetchStations();
    });

    watch(
      () => stationData.value,
      (newValue) => {
        if (newValue && Object.keys(newValue).length > 0) {
          line_data.value = stationData.value.lines[metadata.value.line];
          const env_data = stationData.value.env_data;

          for (const key in actual_env) {
            env[key] = env_data[key];
            actual_env[key] = env_data[key];
          }

          toggle.value = true;

          scores.value.score = cld.calculateScore(line_data.value, env);
          scores.value.average_score = cld.calculateAverageScore(
            line_data.value.light
          );
          data_sizes.value = cld.calculateDelays(line_data.value, env);
          chartArr.value.splice(
            0,
            6,
            ...cld.fillChartArrNew(line_data.value, data_sizes.value, env)
          );
        }
      }
    );

    return {
      startMessage,
      stationData,
      metadata,
      line_data,
      scores,
      data_sizes,
      env,
      actual_env,
      toggle,
      chartArr,
    };
  },
};
</script>
