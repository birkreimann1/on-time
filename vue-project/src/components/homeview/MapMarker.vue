<script setup>
import { ref, watch } from "vue";
import { LCircle } from "@vue-leaflet/vue-leaflet";

// Setup
const emit = defineEmits();
const markerColor = ref("#2563eb");
const marker_radius = ref(20);

// Defines the prop that is send to the parent view
const props = defineProps({
  station: {
    type: Object,
    required: true,
  },
  id: {
    type: String,
    required: true,
  },
  selected: {
    type: Boolean,
    required: true,
  },
});

// Highlights the selected station marker in color and size
watch(
  () => props.selected,
  (newValue) => {
    if (newValue) {
      markerColor.value = "#ff0000";
      marker_radius.value = 30;
    } else {
      markerColor.value = "#2563eb";
      marker_radius.value = 20;
    }
  },
  { immediate: true }
);

//Emits the station id and coordinates of the clicked station marker
const handleClick = () => {
  emit("station-click", props.id, [
    props.station.coords.lat,
    props.station.coords.long,
  ]);
};
</script>

<!-- Creates a circle on each station coordinate -->
<template>
  <l-circle
    :lat-lng="[props.station.coords.lat, props.station.coords.long]"
    :radius="marker_radius"
    :color="markerColor"
    :fill-opacity="0.2"
    :weight="3"
    @click="handleClick"
  />
</template>
