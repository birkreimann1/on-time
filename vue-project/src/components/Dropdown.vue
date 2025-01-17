<template>
  <div class="relative inline-block">
    <!-- Dropdown Trigger Button -->
    <button
      @click="toggleDropdown"
      class="bg-neutral-800 px-4 py-2 rounded-lg w-full text-neutral-200"
    >
      <div class="flex items-center justify-between gap-2">
        <div>
          {{ selectedItem }}
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
      class="absolute mt-1 w-full bg-neutral-900 text-neutral-200 shadow-lg rounded-lg z-50"
    >
      <ul>
        <li
          v-for="(item, index) in items"
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
    items: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      isOpen: false, // Controls dropdown visibility
      selectedItem: this.items[0], // Default to the first item
    };
  },
  methods: {
    toggleDropdown() {
      this.isOpen = !this.isOpen; // Toggle dropdown visibility
    },
    selectItem(item) {
      this.selectedItem = item; // Update the selected item
      this.$emit("select", item); // Emit the selected item
      this.isOpen = false; // Close dropdown after selection
    },
  },
};
</script>
