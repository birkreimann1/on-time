<script setup>
import { ref } from "vue";
import MapMarker from "./MapMarker.vue";
import stationIDs from "../../../datascraping/stationData/station_ids.json";

const emit = defineEmits();
const selectedStationId = ref(null);

const handleStationClick = (stationId, stationCoords) => {
  selectedStationId.value = stationId;
  console.log(stationCoords)
  emit("station-click", stationId, stationCoords);
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
