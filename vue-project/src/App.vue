<script setup>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";
import MapMarkerLayer from "./components/MapMarkerLayer.vue";
import SearchBar from "./components/SearchBar.vue";
</script>

<template>
  <div class="flex flex-col h-screen items-center justify-center">
    <div class="flex flex-col gap-4 bg-black w-full p-6">
      <SearchBar />
    </div>
    <div class="flex flex-grow w-full">
      <l-map
        :use-global-leaflet="false"
        v-model:zoom="zoom"
        :center="[53.8677, 10.68601]"
        style="height: 100%; width: 100%"
      >
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          layer-type="base"
          name="OpenStreetMap"
        />
        <!-- Add the marker here -->
        <MapMarkerLayer />
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
  },
  data() {
    return {
      zoom: 13,
    };
  },
};
</script>
