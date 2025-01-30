<script setup>
import { ref, watch } from "vue";
import MapMarker from "./MapMarker.vue";
import stationIDs from "../../../datascraping/stationData/station_ids.json";

// Setup
const emit = defineEmits();
const selectedStationId = ref(null);
const props = defineProps({
  station: Object,
});

// When a station map marker is clicked emits the coordinates and the id to the parent view
const handleStationClick = (stationId, stationCoords) => {
  selectedStationId.value = stationId;
  emit("station-click", stationId, stationCoords);
};

// Sets the selected station id when a station is clicked within the searchBar.vue
watch(
  () => props.station,
  (newStation) => {
    if (newStation) {
      selectedStationId.value = newStation.id;
    }
  },
  { immediate: true }
);
</script>

<!-- Displays map markers for every station in stationIds.json -->
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
