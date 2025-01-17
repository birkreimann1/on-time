<template>
  <div class="relative">
    <input
      class="bg-neutral-800 text-white p-2 rounded-xl w-full"
      v-model="startMessage"
      placeholder="Start"
      @focus="focused = true"
      @blur="focused = false"
    />

    <!-- Results Dropdown -->
    <div
      v-if="focused && startMessage && filteredList().length"
      class="absolute left-0 w-full bg-neutral-800 text-white p-2 mt-1 rounded-xl shadow-lg"
      style="max-height: 200px; overflow-y: auto; z-index: 10"
    >
      <div
        v-for="entry in filteredList()"
        :key="entry.id"
        class="cursor-pointer p-2 hover:bg-gray-700 rounded"
        @click="handleStationClick(entry)"
      >
        {{ entry.station.name }}
      </div>
    </div>

    <!-- Display Station Data -->
    <div v-if="stationData.length > 0" class="mt-4">
      <h2 class="text-white">Station Data:</h2>
      <div class="station-list-container">
        <ul class="station-list">
          <li
            v-for="item in stationData"
            :key="item.headsign"
            class="station-item"
          >
            <div class="flex flex-grow text-white">
              <span>{{ item.headsign }} - Line {{ item.line.name }} </span>
              <span v-if="item.timeLeft > 0">
                - {{ item.timeLeft }} min left
              </span>
              <span v-else> - Departed</span>
            </div>
            <div class="score-circle flex-grow-0">{{ item.score }}</div>
          </li>
        </ul>
      </div>
    </div>

    <p v-else-if="stationData.length === 0">No data found for this station.</p>
    <p v-else>Loading...</p>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { getDatabase, ref as dbRef, get as dbGet } from "firebase/database";
import stationIds from "../../../datascraping/stationData/station_ids.json";

export default {
  setup() {
    const startMessage = ref(""); // User input for station name
    const stationData = ref([]); // Store station data
    const selectedStationId = ref(null); // Store the selected station's ID
    const stationScores = ref({});
    const generateRandomScore = () => Math.floor(Math.random() * 101);
    const stations = ref();

    const fetchStations = async () => {
      const db = getDatabase();
      const stationsRef = dbRef(db, "stations");

      try {
        const snapshot = await dbGet(stationsRef);
        if (snapshot.exists()) {
          const stationsData = snapshot.val();
          stations.value = {}; // Initialize stations.value as an empty object

          // Loop through each station by its id and assign directly to stations.value
          for (const id in stationsData) {
            if (stationsData.hasOwnProperty(id)) {
              const station = stationsData[id];
              // Directly assign the station data to the corresponding ID in the object
              stations.value[id] = station;
            }
          }
          console.log(stations.value);
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

    stationData.value = stationData.value.map((item) => {
      const departureTime = item.time * 1000; // Convert to milliseconds
      const currentTime = Date.now();
      const timeLeft = Math.max(
        0,
        Math.floor((departureTime - currentTime) / 60000)
      ); // Convert to minutes

      return {
        ...item,
        score: generateRandomScore(), // Add random score
        timeLeft, // Add the calculated time left in minutes
      };
    });

    const fetchStationData = async (id) => {
      const url = `https://thingproxy.freeboard.io/fetch/https://netzplan.swhl.de/api/v1/stationboards/hafas/${id}?v=0&limit=10`;
      try {
        const response = await axios.get(url);
        // Store the data into stationData
        stationData.value = response.data.data || [];

        const station_lines = stations.value[id];
        const score = 100;

        stationData.value = stationData.value.map((item) => {
          const departureTime = item.time * 1000;
          const currentTime = Date.now();
          const timeLeft = Math.max(
            0,
            Math.floor((departureTime - currentTime) / 60000)
          );
          const line = parseInt(item.line.name, 10);
          console.log(line);

          console.log(station_lines);
          const size_day = parseFloat(station_lines[line].light.day.data_size);
          const score_day = parseFloat(station_lines[line].light.day.score);
          const size_night = parseFloat(
            station_lines[line].light.night.data_size
          );
          const score_night = parseFloat(station_lines[line].light.night.score);
          const score =
            (size_day * score_day + size_night * score_night) /
            (size_day + size_night);
          console.log(size_day, score_day, size_night, score_night, score);

          return {
            ...item,
            score: score, // Add random score
            timeLeft, // Add the calculated time left in minutes
          };
        });

        console.log("Station Data with Time Left:", stationData.value);
      } catch (error) {
        console.error(
          "Error fetching station data:",
          error.response || error.message || error
        );
        stationData.value = []; // Reset on error
      }
    };

    // Filter the stations based on the user's input
    const filteredList = () => {
      if (!startMessage.value.trim()) {
        return [];
      }

      // Filter the stations based on the user input
      return Object.entries(stationIds) // Convert object to [key, value] pairs
        .filter(
          ([id, station]) =>
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
      selectedStationId.value = entry.id;
      console.log("Selected station:", entry);
      fetchStationData(entry.id);
      startMessage.value = entry.station.name;
    };

    return {
      startMessage,
      stationData,
      filteredList,
      handleStationClick,
      fetchStationData,
      stations,
    };
  },
};
</script>

<style scoped>
/* Optional: Add some basic styling */
.item.error {
  color: red;
  font-weight: bold;
}

.score-circle {
  width: 30px; /* Circle width */
  height: 30px; /* Circle height */
  border-radius: 50%; /* Make it round */
  background-color: #4caf50; /* You can change this color */
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
  width: 100%; /* Ensure input stretches to full container width */
  max-width: 100%;
}

/* Dropdown Results */
.absolute {
  z-index: 10; /* Ensure the dropdown appears above other content */
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

/* Station List Container */
.station-list-container {
  max-height: 300px; /* Prevent overflowing */
  overflow-y: auto;
  padding-right: 10px; /* Add padding on the right for scrollbar */
}

/* Styling individual items */
.station-item {
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between; /* Space between text and circle */
}

.divider {
  border-top: 1px solid #444;
  margin: 10px 0;
}

/* Optional Styling for Empty Data and Loading */
p {
  color: #ccc;
}

/* Additional Spacing */
.mt-4 {
  margin-top: 20px;
}

/* Styling Error or No Results */
.item.error {
  color: red;
  font-weight: bold;
}
</style>
