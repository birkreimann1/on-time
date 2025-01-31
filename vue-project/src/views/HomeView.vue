<script setup>

// External imports
import "leaflet/dist/leaflet.css";
import { ref } from "vue";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

// Components
import MapMarkerLayer from "../components/homeview/MapMarkerLayer.vue";
import SearchBar from "../components/homeview/SearchBar.vue";

// Setup
const selectedStationId = ref(null);
const center = ref([53.8677, 10.68601]);
const zoom = ref(13);
const selectedStation = ref();
const stationIds = window.stationIds;

// Gives station id to seachBar when station marker is clicked 
// Sets center of map to station marker and sets minimum zoom 
const handleStationClick = (stationId, stationCoords) => {
  center.value = stationCoords;
  zoomOnMarker()
  selectedStationId.value = stationId;
  console.log("Station clicked:", stationId);
};

// Gives station id to seachBar when station is clicked in search results
// Sets center of map to station marker and sets minimum zoom 
const handleStationSearch = (station) => {
  center.value = [station.station.coords.lat, station.station.coords.long];
  zoomOnMarker()
  selectedStation.value = station;
  console.log("Station searched:", station);
};

// Set zoom to a minimum of 16
function zoomOnMarker() {
  if (zoom.value < 16) {
    setTimeout(function () { 
      zoom.value = 16;
    }, 300);
  }
}
</script>

<!-- Main station selection page -->
<template>
  <div class="flex flex-col h-screen">
    <div class="flex flex-grow w-full h-[40%]">

      <!-- Map of available stations -->
      <l-map
        ref="mapRef"
        :use-global-leaflet="false"
        v-model:zoom="zoom"
        :center="center"
        style="height: 100%; width: 100%"
      >
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          layer-type="base"
          name="OpenStreetMap"
        />
        <MapMarkerLayer
          :station="selectedStation"
          :map="mapRef"
          @station-click="handleStationClick"
        />
      </l-map>
    </div>

    <!-- Front page search bar -->
    <div class="flex flex-col bg-black w-full h-[60%]">
      <SearchBar
        @station-click="handleStationSearch"
        :stationsList="stationIds"
        :selectedStationId="selectedStationId"
      />
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
  },
};
</script>
