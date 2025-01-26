<template>
  <div class="flex pl-6 pr-6 items-center h-[20%]">
    <input
      class="bg-neutral-800 text-white p-2 rounded-xl w-full'"
      v-model="startMessage"
      placeholder="Start"
      @focus="focused = true"
      @blur="focused = false"
    />
  </div>

  <!-- Results Dropdown -->
  <div class="top flex">
    <div
      v-if="focused && startMessage && filteredList().length"
      class="fixed w-full bg-neutral-950 text-white pl-6 pr-6 pt-2 shadow-lg max-h-[40%] overflow-auto"
    >
      <div
        v-for="entry in filteredList()"
        :key="entry.id"
        class="cursor-pointer p-1.5 hover:bg-gray-700 rounded mb-2"
        @click="handleStationClick(entry)"
      >
        {{ entry.station.name }}
      </div>
    </div>
  </div>

  <div
    v-if="errorMessage"
    class="text-red-500 flex w-full overflow-auto p-6 bg-neutral-900 h-[80%]"
  >
    {{ errorMessage }}
  </div>

  <div
    v-if="!errorMessage"
    class="w-full overflow-auto bg-neutral-900 p-6 h-[80%]"
  >
    <ul class="station-list">
      <li
        v-for="item in stationData"
        :key="item.headsign"
        class="station-item cursor-pointer"
        @click="handleScoreClick(item)"
      >
        <div>
          <p class="font-bold">{{ item.line.name }} - {{ item.headsign }}</p>
          <p v-if="item.timeLeft > 0">In {{ item.timeLeft }} min</p>
          <p v-else>Bereits abgefahren</p>
        </div>
        <div
          class="score-circle flex-grow-0"
          :style="{ backgroundColor: getScoreColor(item.score) }"
        >
          {{ item.score }}
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { getDatabase, ref as dbRef, get as dbGet } from "firebase/database";
import stationIds from "../../../datascraping/stationData/station_ids.json";
import { calculateScore } from "../utils/calculateLineData";

export default {
  props: {
    selectedStationId: {
      type: [String, Number],
      required: true,
    },
  },
  computed: {
    scoreColor() {
      return this.getScoreColor(this.item.score);
    },
  },
  methods: {
    getScoreColor(score) {
      if (score >= 97) {
        return "#397d3b";
      } else if (score >= 95) {
        return "#d9ad1e";
      } else if (score >= 93) {
        return "#b3721d";
      } else {
        return "#8f2c25";
      }
    },
  },
  emits: ["station-click"],
  setup(props, { emit }) {
    const router = useRouter();
    const startMessage = ref("");
    const stationData = ref([]);
    const stations = ref();
    const errorMessage = ref("");

    const handleScoreClick = (item) => {
      console.log("Score circle clicked for item:", item);

      router.push({
        path: "/score",
        query: {
          name: item.name,
          id: item.id,
          line: item.line.name,
          headsign: item.headsign,
        },
      });
    };

    const fetchStations = async () => {
      const db = getDatabase();
      const stationsRef = dbRef(db, "stations");

      try {
        const snapshot = await dbGet(stationsRef);
        if (snapshot.exists()) {
          const stationsData = snapshot.val();
          stations.value = {};

          for (const id in stationsData) {
            if (stationsData.hasOwnProperty(id)) {
              const station = stationsData[id];
              stations.value[id] = station;
            }
          }
        } else {
          console.log("No data available");
        }
      } catch (error) {
        console.error("Error fetching data from Firebase:", error);
      }
    };

    onMounted(() => {
      fetchStations(); // Fetch station data when component is mounted
    });

    watch(
      () => props.selectedStationId,
      (newId) => {
        if (newId) {
          fetchStationData(newId);
          startMessage.value = stationIds[newId].name;
        }
      }
    );

    const fetchStationData = async (id) => {
      const url = `https://thingproxy.freeboard.io/fetch/https://netzplan.swhl.de/api/v1/stationboards/hafas/${id}?v=0&limit=10`;
      console.log("API Request:", url);
      errorMessage.value = "";

      try {
        const response = await axios.get(url);

        // Log the response to verify data structure
        console.log("API Response:", response);

        // Check if data is available before mapping
        if (
          !response.data ||
          !response.data.data ||
          response.data.data.length === 0
        ) {
          console.log("No data available from API");
          return;
        }

        stationData.value = response.data.data || [];

        // Now map through stationData only after data is fetched
        stationData.value = stationData.value.map((item) => {
          const departureTime = item.time * 1000;
          const currentTime = Date.now();
          const timeLeft = Math.max(
            0,
            Math.floor((departureTime - currentTime) / 60000)
          );
          const line = parseInt(item.line.name, 10);
          const line_data = stations.value[id].lines[line];
          const env_data = stations.value[id].env_data;

          let score = calculateScore(line_data, env_data);

          return {
            ...item,
            id,
            score,
            timeLeft,
          };
        });
      } catch (error) {
        console.error("Error fetching station data:", error);
        stationData.value = [];
        errorMessage.value = "Keine Einträge verfügbar!";
      }
    };

    const filteredList = () => {
      if (!startMessage.value.trim()) {
        return [];
      }

      // Filter the stations based on the user input
      return Object.entries(stationIds)
        .filter(
          (station) =>
            station.name
              .toLowerCase()
              .includes(startMessage.value.toLowerCase()) // Filter by name
        )
        .map(([id, station]) => ({
          id,
          station,
        }));
    };

    // Handle the click event for a station from the filtered list
    const handleStationClick = (entry) => {
      startMessage.value = entry.station.name;
      console.log("Selected station:", entry);
      fetchStationData(entry.id);
      emit("station-click", entry);
    };

    return {
      startMessage,
      stationData,
      filteredList,
      handleStationClick,
      fetchStationData,
      stations,
      handleScoreClick,
      errorMessage,
    };
  },
};
</script>

<style scoped>
.score-circle {
  width: 40px;
  /* Circle width */
  height: 40px;
  /* Circle height */
  border-radius: 50%;
  /* Make it round */
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.relative {
  position: relative;
  padding: 20px;
}

input {
  width: 100%;
  /* Ensure input stretches to full container width */
  max-width: 100%;
}

/* Dropdown Results */
.absolute {
  z-index: 10;
  /* Ensure the dropdown appears above other content */
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

/* Styling individual items */
.station-item {
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* Space between text and circle */
}

/* Optional Styling for Empty Data and Loading */
p {
  color: #ccc;
}
</style>
