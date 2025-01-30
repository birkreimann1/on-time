<template>

  <!-- Search Input -->
  <div class="flex pl-6 pr-6 items-center h-[20%]">
    <input class="bg-neutral-800 text-white p-2 rounded-xl w-full" v-model="startMessage" placeholder="Start"
      @focus="focused = true" @blur="focused = false" />
  </div>

  <!-- Search Results Dropdown -->
  <div class="top flex">
    <div v-if="focused && startMessage && filteredList().length"
      class="fixed w-full bg-neutral-950 text-white pl-6 pr-6 pt-2 shadow-lg max-h-[40%] overflow-auto">
      <div v-for="entry in filteredList()" :key="entry.id" class="cursor-pointer p-1.5 hover:bg-gray-700 rounded mb-2"
        @click="handleStationClick(entry)">
        {{ entry.station.name }}
      </div>
    </div>
  </div>

  <!-- Error message when no departure data could be fetched -->
  <div v-if="errorMessage" class="text-red-500 flex w-full overflow-auto p-6 bg-neutral-900 h-[80%]">
    {{ errorMessage }}
  </div>

  <!-- List of the fetched departures of the searched or clicked station -->
  <div v-if="!errorMessage" class="w-full overflow-auto bg-neutral-900 p-6 h-[80%]">
    <ul class="station-list">
      <li v-for="item in stationDepartures" :key="item.id"
        class="station-item cursor-pointer flex items-center justify-between p-2.5" @click="handleDepartureClick(item)">
        <div>
          <p class="font-bold">{{ item.line.name }} - {{ item.headsign }}</p>
          <p v-if="item.timeLeft > 0">In {{ item.timeLeft }} min</p>
          <p v-else>Bereits abgefahren</p>
        </div>
        <div class="flex items-center justify-center w-10 h-10 rounded-full font-bold"
          :style="{ backgroundColor: scoreColor(item.score) }">
          {{ item.score }}
        </div>
      </li>
    </ul>
  </div>

</template>

<script>
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import stationIds from "../../../datascraping/stationData/station_ids.json";
import { getScoreColor } from '../utils/scoreColor';
import { fetchStationData } from '../utils/fetchStationData';
import { fetchStationDepartures } from '../utils/fetchStationDepartures';

export default {

  // ID of the station clicked on the map
  props: {
    selectedStationId: {
      type: [String, Number],
      required: true,
    },
  },

  // Colors the score display
  methods: {
    scoreColor(score) {
      return getScoreColor(score);
    },
  },

  // Emits the searched station to the parent view
  emits: ["station-click"],

  // Main setup of the component
  setup(props, { emit }) {
    const router = useRouter();
    const startMessage = ref("");
    const stationDepartures = ref([]);
    const stationData = ref();
    const errorMessage = ref("");

    // When a departure is clicked routes to the corresponding score page
    const handleDepartureClick = (item) => {
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

    // Get the collected data from firebase when the website is loaded
    onMounted(() => {
      fetchStationData(stationData);
    });

    // Fetches the station departures when a station is clicked on the map
    watch(
      () => props.selectedStationId,
      (newId) => {
        if (newId) {
          fetchStationDeparturesData(newId);
          startMessage.value = stationIds[newId].name;
        }
      }
    );

    // Fetch the next departures for the station with the corresponding id
    const fetchStationDeparturesData = async (id) => {
      const { stationDeparturesData, errorMsg } = await fetchStationDepartures(id, stationData.value);
      stationDepartures.value = stationDeparturesData;
      errorMessage.value = errorMsg;
    };

    // Filter the stationIds.json by name and return matching stations
    const filteredList = () => {
      if (!startMessage.value.trim()) {
        return [];
      }

      return Object.entries(stationIds)
        .filter(
          ([id, station]) =>
            station.name
              .toLowerCase()
              .includes(startMessage.value.toLowerCase())
        )
        .map(([id, station]) => ({
          id,
          station,
        }));
    };

    // Fetches the departure data of the clicked station inside the seach result dropdown
    const handleStationClick = (entry) => {
      startMessage.value = entry.station.name;
      console.log("Selected station:", entry);
      fetchStationDeparturesData(entry.id);
      emit("station-click", entry);
    };

    return {
      startMessage,
      stationDepartures,
      filteredList,
      handleStationClick,
      fetchStationDeparturesData,
      stationData,
      handleDepartureClick,
      errorMessage,
    };
  },
};
</script>