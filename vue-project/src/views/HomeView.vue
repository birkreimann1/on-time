<script setup>
import { ref } from "vue";
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";
import MapMarkerLayer from "../components/MapMarkerLayer.vue";
import SearchBar from "../components/SearchBar.vue";
import stationIDs from "../../../datascraping/stationData/station_ids.json";

// Reactive variable to hold the selected station's ID
const selectedStationId = ref(null);
const center = ref([53.8677, 10.68601])
const zoom = ref(13)

const handleStationClick = (stationId, stationCoords) => {

  center.value = stationCoords
  if (zoom.value < 16) {
    setTimeout(function () {
      zoom.value = 16
    }, 300);
  }

  selectedStationId.value = stationId;
  console.log("Station clicked:", stationId);
};
</script>

<template>
  <div class="flex flex-col h-screen items-center justify-center">
    <div class="flex flex-col gap-4 bg-black w-full p-6 max-h-[50%]">
      <SearchBar
        @station-click="handleStationClick"
        :stationsList="stationIDs"
        :selectedStationId="selectedStationId"
      />
    </div>
    <div class="flex flex-grow w-full max-h-[100%]">
      <l-map ref="mapRef" :use-global-leaflet="false" v-model:zoom="zoom" :center="center"
        style="height: 100%; width: 100%">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base" name="OpenStreetMap" />
        <MapMarkerLayer :stations="stationIDs" :map="mapRef" @station-click="handleStationClick" />
      </l-map>
    </div>
  </div>
</template>

<script>
export default {
  components: {
    LMap,
    LTileLayer,
    MapMarkerLayer,
    SearchBar,
  }
};
</script>
