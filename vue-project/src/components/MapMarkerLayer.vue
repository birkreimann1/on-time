<script setup>
import { ref } from "vue";
import MapMarker from "./MapMarker.vue";
import stationIDs from "../../../datascraping/stationData/station_ids.json";

// Define the emit function
const emit = defineEmits();

// Keep track of selected station's id
const selectedStationId = ref(null);

// Handle the station click event to update the selected station
const handleStationClick = (stationId) => {
  // Update selected station id
  selectedStationId.value = stationId;
  // Emit the station-click event
  emit("station-click", stationId);
};
</script>

<template>
  <MapMarker
    v-for="(station, key) in stationIDs"
    :key="key"
    :id="key"
    :station="station"
    :selected="key === selectedStationId"
    @station-click="handleStationClick"
  />
</template>
