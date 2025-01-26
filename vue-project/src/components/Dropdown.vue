<template>
  <div class="relative inline-block">
    <!-- Dropdown Trigger Button -->
    <button
      @click="toggleDropdown"
      class="bg-neutral-800 px-4 py-2 rounded-lg w-full text-neutral-200"
    >
      <div class="flex items-center justify-between gap-2">
        <div>
          {{ translatedSelectedItem }}
        </div>
        <div>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 512 512"
            height="16"
            width="16"
            class="fill-white"
          >
            <path
              d="M233.4 406.6c12.5 12.5 32.8 12.5 45.3 0l192-192c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L256 338.7 86.6 169.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l192 192z"
            />
          </svg>
        </div>
      </div>
    </button>

    <!-- Dropdown Menu -->
    <div
      v-if="isOpen"
      class="absolute mt-1 w-full bg-pink-900 text-neutral-200 shadow-lg rounded-lg z-50"
    >
      <ul>
        <li
          v-for="(item, index) in availableItems"
          :key="index"
          @click="selectItem(item)"
          class="px-4 py-2 cursor-pointer"
        >
          {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    actualEnv: {
      type: Array,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isOpen: false,
      selectedItem: this.actualEnv, // Use the raw string value
      availableItems: this.getAvailableItems(),
    };
  },
  computed: {
    // Translated selected item for display
    translatedSelectedItem() {
      return this.getTranslatedLabel(this.selectedItem);
    },
  },
  watch: {
    actualEnv: {
      handler(newVal) {
        this.selectedItem = newVal;
      },
      immediate: true,
    },
  },
  methods: {
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },
    selectItem(item) {
      this.selectedItem = item; // Update selected item
      this.$emit("select", item); // Emit the selected value
      this.isOpen = false; // Close the dropdown
    },
    getAvailableItems() {
      const displayValues = {
        light: {
          null: "Keine Auswahl",
          day: "Tag",
          night: "Nacht",
        },
        temp: {
          null: "Keine Auswahl",
          freezing: "unter 0 °C",
          cool: "0 - 10 °C",
          mild: "10 - 20 °C",
          warm: "20 - 30 °C",
          hot: "über 30 °C",
        },
        traffic: {
          null: "Keine Auswahl",
          work: "Berufsverkehr",
          free: "Freizeitverkehr",
          offwork: "Ruhiger Verkehr",
        },
        weather: {
          null: "Keine Auswahl",
          clear: "Klar",
          clouds: "Bedeckt",
          rain: "Regen",
          fog: "Nebel",
          snow: "Schnee",
          storm: "Sturm",
          thunderstorm: "Gewitter",
        },
      };

      // Map the raw values to human-readable labels
      return Object.keys(displayValues[this.label] || {}).map(
        (key) => displayValues[this.label][key]
      );
    },
    getTranslatedLabel(rawValue) {
      const displayValues = {
        light: {
          null: "Keine Auswahl",
          day: "Tag",
          night: "Nacht",
        },
        temp: {
          null: "Keine Auswahl",
          freezing: "unter 0 °C",
          cool: "0 - 10 °C",
          mild: "10 - 20 °C",
          warm: "20 - 30 °C",
          hot: "über 30 °C",
        },
        traffic: {
          null: "Keine Auswahl",
          work: "Berufsverkehr",
          free: "Freizeitverkehr",
          offwork: "Ruhiger Verkehr",
        },
        weather: {
          null: "Keine Auswahl",
          clear: "Klar",
          clouds: "Bedeckt",
          rain: "Regen",
          fog: "Nebel",
          snow: "Schnee",
          storm: "Sturm",
          thunderstorm: "Gewitter",
        },
      };

      // Return the translated label for the raw value
      return displayValues[this.label][rawValue] || rawValue;
    },
  },
};
</script>
