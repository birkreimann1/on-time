<script setup>
import { defineProps, defineEmits, ref, watch } from "vue";
import { LCircle } from "@vue-leaflet/vue-leaflet";

// Define the props and emits
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

const emit = defineEmits(); // Use this to emit events

// Local marker color, based on selection state
const markerColor = ref("#2563eb");
const marker_radius = ref(20);

// Watch for changes in the selected prop and update marker color and radius
watch(
  () => props.selected,
  (newValue) => {
    if (newValue) {
      markerColor.value = "#ff0000"; // Red for selected
      marker_radius.value = 30; // Larger size for selected
    } else {
      markerColor.value = "#2563eb"; // Default color (blue)
      marker_radius.value = 20; // Default size
    }
  },
  { immediate: true }
);

// Emit station-click event to parent
const handleClick = () => {
  emit("station-click", props.id, [props.station.coords.lat, props.station.coords.long]);
};
</script>

<template>
  <!-- Use LCircle component from vue-leaflet to render the marker -->
  <l-circle
    :lat-lng="[props.station.coords.lat, props.station.coords.long]"
    :radius="marker_radius"
    :color="markerColor"
    :fill-opacity="0.2"
    :weight="3"
    @click="handleClick"
  />
</template>
