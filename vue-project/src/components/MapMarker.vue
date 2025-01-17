<script setup>
import { LCircle } from "@vue-leaflet/vue-leaflet";
import { defineProps } from "vue";

const props = defineProps({
  station: {
    type: Object,
    required: true,
  },
  id: {
    type: String,
    required: true,
  },
});

const emit = defineEmits();

const handleClick = () => {
  const stationId = props.id;
  emit("station-click", stationId);
};
</script>

<template>
  <l-circle
    :lat-lng="[props.station.coords.lat, props.station.coords.long]"
    :radius="20"
    :options="{
      color: '#2563eb', // Border color of the circle
      fillOpacity: 0.2, // Opacity of the fill color
      weight: 3, // Border width
    }"
    @click="handleClick"
  />
</template>
