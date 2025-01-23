<template>
  <div class="bg-black h-screen text-white p-8">
    <!-- Question Mark Button -->
    <div class="flex justify-end">
      <button class="p-2 bg-neutral-800 rounded-lg" @click="togglePopup">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" class="fill-white" height="32" width="32">
          <path
            d="M80 160c0-35.3 28.7-64 64-64l32 0c35.3 0 64 28.7 64 64l0 3.6c0 21.8-11.1 42.1-29.4 53.8l-42.2 27.1c-25.2 16.2-40.4 44.1-40.4 74l0 1.4c0 17.7 14.3 32 32 32s32-14.3 32-32l0-1.4c0-8.2 4.2-15.8 11-20.2l42.2-27.1c36.6-23.6 58.8-64.1 58.8-107.7l0-3.6c0-70.7-57.3-128-128-128l-32 0C73.3 32 16 89.3 16 160c0 17.7 14.3 32 32 32s32-14.3 32-32zm80 320a40 40 0 1 0 0-80 40 40 0 1 0 0 80z" />
        </svg>
      </button>
    </div>

    <!-- Main Content -->
    <div class="flex flex-col gap-12 pb-8">
      <!-- Score Circles -->
      <div class="flex justify-center items-end">
        <div class="flex flex-col items-end text-center gap-2">
          <div class="flex justify-center w-full">
            <div class="h-32 w-32 rounded-full bg-green-600 flex justify-center items-center"
              :style="{ backgroundColor: getScoreColor(score) }">
              <div class="h-[120px] w-[120px] rounded-full bg-black flex justify-center items-center text-6xl">
                {{ scores.score }}
              </div>
            </div>
          </div>
          <div>Score mit aktuellen Bedingungen</div>
        </div>
        <div class="flex flex-col items-center gap-2">
          <div class="h-20 w-20 rounded-full bg-yellow-500 flex justify-center items-center"
            :style="{ backgroundColor: getScoreColor(average_score) }">
            <div class="h-[72px] w-[72px] rounded-full bg-black flex justify-center items-center text-3xl">
              {{ scores.average_score }}
            </div>
          </div>
          <div class="text-center">Score im Durchschnitt</div>
        </div>
      </div>

      <!-- Additional Information -->
      <div class="flex flex-col gap-12">
        <div class="flex justify-center text-3xl font-bold text-white">
          {{ metadata.headsign }}
        </div>
        <div class="flex justify-between items-center">
          <div class="flex gap-4">
            <input type="checkbox" v-model="toggle" true-value="yes" false-value="no" class="scale-150" />
            <div>aktuelle Bedingungen</div>
          </div>
          <button class="p-2 bg-neutral-800 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="fill-white" height="32" width="32">
              <path
                d="M495.9 166.6c3.2 8.7 .5 18.4-6.4 24.6l-43.3 39.4c1.1 8.3 1.7 16.8 1.7 25.4s-.6 17.1-1.7 25.4l43.3 39.4c6.9 6.2 9.6 15.9 6.4 24.6c-4.4 11.9-9.7 23.3-15.8 34.3l-4.7 8.1c-6.6 11-14 21.4-22.1 31.2c-5.9 7.2-15.7 9.6-24.5 6.8l-55.7-17.7c-13.4 10.3-28.2 18.9-44 25.4l-12.5 57.1c-2 9.1-9 16.3-18.2 17.8c-13.8 2.3-28 3.5-42.5 3.5s-28.7-1.2-42.5-3.5c-9.2-1.5-16.2-8.7-18.2-17.8l-12.5-57.1c-15.8-6.5-30.6-15.1-44-25.4L83.1 425.9c-8.8 2.8-18.6 .3-24.5-6.8c-8.1-9.8-15.5-20.2-22.1-31.2l-4.7-8.1c-6.1-11-11.4-22.4-15.8-34.3c-3.2-8.7-.5-18.4 6.4-24.6l43.3-39.4C64.6 273.1 64 264.6 64 256s.6-17.1 1.7-25.4L22.4 191.2c-6.9-6.2-9.6-15.9-6.4-24.6c4.4-11.9 9.7-23.3 15.8-34.3l4.7-8.1c6.6-11 14-21.4 22.1-31.2c5.9-7.2 15.7-9.6 24.5-6.8l55.7 17.7c13.4-10.3 28.2-18.9 44-25.4l12.5-57.1c2-9.1 9-16.3 18.2-17.8C227.3 1.2 241.5 0 256 0s28.7 1.2 42.5 3.5c9.2 1.5 16.2 8.7 18.2 17.8l12.5 57.1c15.8 6.5 30.6 15.1 44 25.4l55.7-17.7c8.8-2.8 18.6-.3 24.5 6.8c8.1 9.8 15.5 20.2 22.1 31.2l4.7 8.1c6.1 11 11.4 22.4 15.8 34.3zM256 336a80 80 0 1 0 0-160 80 80 0 1 0 0 160z" />
            </svg>
          </button>
        </div>
        <div class="flex justify-center gap-4">
          <div class="flex flex-col gap-4 items-end">
            <div>Fahrten insgesamt</div>
            <div>davon Verspätungen</div>
            <div>Durchschnittsverspätung</div>
          </div>
          <div class="flex flex-col gap-4">
            <div>{{ line_data?.totalTrips || 'N/A' }}</div>
            <div>{{ line_data?.delayedTrips || 'N/A' }}</div>
            <div>{{ line_data?.averageDelay || 'N/A' }} min</div>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
          <p>Lichtverhältnisse</p>
          <Dropdown :actualEnv="env.light" label="light" @select="handleSelection('light', $event)" />
        </div>
        <div class="flex flex-col gap-1">
          <p>Temperatur</p>
          <Dropdown :actualEnv="env.temp" label="temp" @select="handleSelection('temp', $event)" />
        </div>
        <div class="flex flex-col gap-1">
          <p>Verkehr</p>
          <Dropdown :actualEnv="env.traffic" label="traffic" @select="handleSelection('traffic', $event)" />
        </div>
        <div class="flex flex-col gap-1">
          <p>Wetter</p>
          <Dropdown :actualEnv="env.weather" label="weather" @select="handleSelection('weather', $event)" />
        </div>
      </div>
    </div>

    <!-- Popup -->
    <div v-if="showPopup" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div class="bg-neutral-800 text-neutral-200 p-8 rounded-lg shadow-lg w-full">
        <div class="flex justify-between mb-4">
          <h2 class="text-xl font-bold">Wie setzt sich der Score zusammen?</h2>
          <div>
            <button @click="togglePopup" class="p-1 bg-neutral-900 rounded-lg flex-grow-0">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" class="fill-white" height="32" width="32">
                <path
                  d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z" />
              </svg>
            </button>
          </div>
        </div>
        <p class="font-bold text-xl">Attribute</p>
        <ul>
          <li>Licht</li>
          <li>Temperatur</li>
          <li>Verkehr</li>
          <li>Wetter</li>
        </ul>
        <p class="font-bold text-xl pt-4">Berechnung</p>
        <p>a² + b² = c²</p>
      </div>
    </div>
  </div>
</template>

<script>
import Dropdown from "../components/Dropdown.vue";
import { useRoute } from "vue-router";
import { ref, onMounted, watch, reactive } from "vue";
import { getDatabase, ref as dbRef, get as dbGet } from "firebase/database";
import { calculateScore, calculateAverageScore } from "../utils/calculateLineData";
import { getRawValue } from "../utils/translateLabelToRaw"

export default {
  components: {
    Dropdown,
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
      this.showPopup = !this.showPopup; // Toggle popup visibility
    },
    toggleDropdown() {
      this.isOpen = !this.isOpen; // Toggle dropdown visibility
    },
    getScoreColor(score) {
      if (score >= 97) {
        return "#397d3b";
      } else if (score >= 95) {
        return "#d9ad1e";
      } else if (score >= 93) {
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
      this.scores.score = calculateScore(this.line_data, this.env);
    },
  },
  setup() {
    const route = useRoute();
    const startMessage = ref("");
    const stationData = ref([]);
    const metadata = ref({
      id: null,
      line: null,
      headsign: null,
    });
    const scores = ref({
      score: null,
      average_score: null
    });
    const line_data = ref(null);
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

    const fetchStations = async () => {
      const db = getDatabase();
      const stationsRef = dbRef(db, `stations/${String(metadata.value.id)}`);

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
        console.log("Id:", metadata.value.id, "\nLine:", metadata.value.line, "\nHeadsign:", metadata.value.headsign);
      } else {
        console.log("No id found in route query.");
      }

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
          console.log(env)

          toggle.value = true;

          scores.value.score = calculateScore(line_data.value, env);
          scores.value.average_score = calculateAverageScore(line_data.value.light);
        }
      }
    );

    return {
      startMessage,
      stationData,
      metadata,
      scores,
      line_data,
      env,
      toggle
    };
  },
};
</script>
