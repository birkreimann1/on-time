<script setup>
</script>

<!-- <template>
  <div className="flex flex-col h-screen items-center justify-center">
      <div className="flex flex-col gap-4 bg-black w-full p-6">
        <div className="w-full bg-neutral-800 p-4 rounded-full text-neutral-400">Start</div>
        <div className="w-full bg-neutral-800 p-4 rounded-full text-neutral-400">Ziel</div>
      </div>
      <div className="flex flex-grow justify-center items-center bg-green-700 w-full">Map</div>
    </div>
</template> -->



<template>
  <div class="xyz">
    <l-map :use-global-leaflet="false" ref="map" v-model:zoom="zoom" :center="[47.41322, -1.219482]">
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
      ></l-tile-layer>
    </l-map>
  </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
  },
  data() {
    return {
      zoom: 2,
    };
  },
};
</script>

<style>
.xyz {
    height: 600px;
    width: 800px;
  }</style>