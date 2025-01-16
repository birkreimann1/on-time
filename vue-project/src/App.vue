<script setup></script>

<template>
  <div class="flex flex-col h-screen items-center justify-center">
    <div class="flex flex-col gap-4 bg-black w-full p-6">
      <input
        class="bg-neutral-800 text-white p-2 rounded-xl"
        v-model="message"
        placeholder="Start"
      />
      <input
        class="bg-neutral-800 text-white p-2 rounded-xl"
        v-model="message"
        placeholder="Ziel"
      />
    </div>
    <div className="flex flex-grow w-full">
      <l-map
        :use-global-leaflet="false"
        ref="map"
        v-model:zoom="zoom"
        :center="[53.8677, 10.68601]"
      >
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          layer-type="base"
          name="OpenStreetMap"
        ></l-tile-layer>
      </l-map>
    </div>
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
      zoom: 13,
    };
  },
};
</script>
