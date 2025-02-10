
<!-- Delay details -->
<template>
  <div class="flex justify-center gap-4">

    <!-- Titles -->
    <div class="flex flex-col gap-4 items-start">
      <div>Einbezogene Fahrten</div>
      <div>davon Verspätungen</div>
      <div>Verspätungsrate</div>
      <div>Verspätung (Ø)</div>
      <div>Erwartete Verspätung</div>
    </div>
    
    <div class="border-l border-gray-300"></div>

    <!-- Displayed values -->
    <div class="flex flex-col gap-4">
      <div>{{ dataSizes.size || "0" }}</div>
      <div>{{ dataSizes.delays || "0" }}</div>
      <div>{{ dataSizes.incidence || "N/A" }}</div>
      <div>{{ dataSizes.average_delay }}</div>
      <div>{{ dataSizes.expected_delay }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dataSizes: {
      type: Object,
      required: true,
    },
  },
};
</script>