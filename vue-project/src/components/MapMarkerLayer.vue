<script setup>
import MapMarker from "./MapMarker.vue";
import stationIDs from "../../../datascraping/stationData/station_ids.json";
</script>

<template>
  <MapMarker
    v-for="(station, key) in stationIDs"
    :key="key"
    :station="station"
  />
</template>

<script>
export default {
  components: {
    MapMarker,
  },
};
</script>
