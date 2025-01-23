<script setup>
import { ref, watch } from "vue";
import MapMarker from "./MapMarker.vue";
import stationIDs from "../../../datascraping/stationData/station_ids.json";

const props = defineProps({
  station: Object,
});

const emit = defineEmits();
const selectedStationId = ref(null);

const handleStationClick = (stationId, stationCoords) => {
  selectedStationId.value = stationId;
  console.log(stationCoords)
  emit("station-click", stationId, stationCoords);
};

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
