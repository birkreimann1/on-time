<script setup>
import MapMarker from "./MapMarker.vue";
import stationIDs from "../../../datascraping/stationData/station_ids.json";
</script>

<template>
  <MapMarker
    v-for="(station, key) in stationIDs"
    :id="key"
    :station="station"
    @station-click="handleStationClick"
  />
</template>

<script>
export default {
  methods: {
    handleStationClick(stationId) {
      this.$emit("station-click", stationId);
    },
  },
};
</script>
