
<!-- Enviroment dropdown menus -->
<template>
    <div class="flex flex-col gap-4">

          <!-- Lichtverhältnisse -->
          <div class="flex flex-col gap-1">
            <p>Lichtverhältnisse</p>
            <Dropdown :actualEnv="env.light" label="light" @select="handleSelection('light', $event)" />
          </div>

          <!-- Temperatur -->
          <div class="flex flex-col gap-1">
            <p>Temperatur</p>
            <Dropdown :actualEnv="env.temp" label="temp" @select="handleSelection('temp', $event)" />
          </div>

          <!-- Verkehr -->
          <div class="flex flex-col gap-1">
            <p>Verkehr</p>
            <Dropdown :actualEnv="env.traffic" label="traffic" @select="handleSelection('traffic', $event)" />
          </div>

          <!-- Wetter -->
          <div class="flex flex-col gap-1">
            <p>Wetter</p>
            <Dropdown :actualEnv="env.weather" label="weather" @select="handleSelection('weather', $event)" />
          </div>
        </div>

  </template>
  
  <script>
  import Dropdown from '../control/Dropdown.vue';
  
  export default {

    // Raw and display value for enviroment variable
    props: {
      env: {
        type: Object,
        required: true,
      },
      label: {
        type: String,
        required: true,
      },
    },
    components: {
      Dropdown,
    },
    methods: {

      // Emits selection to parent view
      handleSelection(category, selectedValue) {
        this.$emit('select', category, selectedValue);
      },
    },
  };
  </script>
  