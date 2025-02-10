
<!-- Dropdown element -->
<template>
  <div class="relative inline-block">

    <!-- Dropdown Trigger Button -->
    <button
      @click="toggleDropdown"
      class="bg-neutral-800 px-4 py-2 rounded-lg w-full text-neutral-200"
    >
      <div class="flex items-center justify-between gap-2">
        <span>{{ displayValue }}</span>
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
    </button>

    <!-- Dropdown Menu -->
    <div
      v-if="isOpen"
      class="absolute mt-1 w-full bg-neutral-900 text-neutral-200 shadow-lg rounded-lg z-50"
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
import { getAvailableItems, getDisplayValue } from '../../utils/enviromentValues';

export default {

  // Actual enviromental data and category of the dropdown menu
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

  // Internal states of the dropdown menu
  data() {
    return {
      isOpen: false,
      selectedItem: this.actualEnv,
    };
  },

  computed: {

    // Gets all available items of a category
    availableItems() {
      return getAvailableItems(this.label);
    },

    // Gets display value of selected item
    displayValue() {
      return getDisplayValue(this.selectedItem, this.label);
    },
  },

  // Selects correct dropdown options when enviroment is changed from scoreView.vue
  watch: {
    actualEnv: {
      handler(newVal) {
        this.selectedItem = newVal;
      },
      immediate: true,
    },
  },

  methods: {

    // Close dropdown menu on click when it was open before 
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },

    // Emits selected item of dropdown menu to scoreView.vue and closes dropdown menu
    selectItem(item) {
      this.selectedItem = item;
      this.$emit('select', item);
      this.isOpen = false;
    },
  },
};
</script>
