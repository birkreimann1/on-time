<template>
  <div class="bg-black h-screen text-white p-8">
    <!-- Question Mark Button -->
    <div class="flex justify-end">
      <button class="p-2 bg-neutral-800 rounded-lg" @click="togglePopup">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 320 512"
          class="fill-white"
          height="32"
          width="32"
        >
          <path
            d="M80 160c0-35.3 28.7-64 64-64l32 0c35.3 0 64 28.7 64 64l0 3.6c0 21.8-11.1 42.1-29.4 53.8l-42.2 27.1c-25.2 16.2-40.4 44.1-40.4 74l0 1.4c0 17.7 14.3 32 32 32s32-14.3 32-32l0-1.4c0-8.2 4.2-15.8 11-20.2l42.2-27.1c36.6-23.6 58.8-64.1 58.8-107.7l0-3.6c0-70.7-57.3-128-128-128l-32 0C73.3 32 16 89.3 16 160c0 17.7 14.3 32 32 32s32-14.3 32-32zm80 320a40 40 0 1 0 0-80 40 40 0 1 0 0 80z"
          />
        </svg>
      </button>
    </div>

    <!-- Main Content -->
    <div class="flex flex-col gap-12">
      <!-- Score Circles -->
      <div class="flex justify-center items-end">
        <div class="flex flex-col items-end text-center gap-2">
          <div class="flex justify-center w-full">
            <div
              class="h-32 w-32 rounded-full bg-green-600 flex justify-center items-center"
            >
              <div
                class="h-[120px] w-[120px] rounded-full bg-black flex justify-center items-center text-6xl"
              >
                95
              </div>
            </div>
          </div>
          <div>Score mit aktuellen Bedingungen</div>
        </div>
        <div class="flex flex-col items-center gap-2">
          <div
            class="h-20 w-20 rounded-full bg-yellow-500 flex justify-center items-center"
          >
            <div
              class="h-[72px] w-[72px] rounded-full bg-black flex justify-center items-center text-3xl"
            >
              67
            </div>
          </div>
          <div class="text-center">Score im Durchschnitt</div>
        </div>
      </div>

      <!-- Additional Information -->
      <div class="flex flex-col gap-12">
        <div class="flex justify-center text-3xl font-bold">ZOB Lübeck</div>
        <div class="flex justify-center items-center gap-8">
          <div class="flex gap-4">
            <input
              type="checkbox"
              v-model="toggle"
              true-value="yes"
              false-value="no"
              class="scale-150"
            />
            <div>aktuelle Bedingungen</div>
          </div>
          <button>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 512 512"
              fill="#fff"
              height="32"
              width="32"
            >
              <path
                d="M3.9 54.9C10.5 40.9 24.5 32 40 32l432 0c15.5 0 29.5 8.9 36.1 22.9s4.6 30.5-5.2 42.5L320 320.9 320 448c0 12.1-6.8 23.2-17.7 28.6s-23.8 4.3-33.5-3l-64-48c-8.1-6-12.8-15.5-12.8-25.6l0-79.1L9 97.3C-.7 85.4-2.8 68.8 3.9 54.9z"
              />
            </svg>
          </button>
        </div>
        <div class="flex justify-center gap-4">
          <div class="flex flex-col gap-4 items-end">
            <div>Fahrten insgesamt</div>
            <div>davon Verspätungen</div>
            <div>Durchschnittsverspätung</div>
          </div>
          <div class="flex flex-col gap-4">
            <div>x</div>
            <div>y</div>
            <div>z min</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Popup -->
    <div
      v-if="showPopup"
      class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center"
    >
      <div
        class="bg-neutral-800 text-neutral-200 p-8 rounded-lg shadow-lg w-full"
      >
        <div class="flex justify-between mb-4">
          <h2 class="text-xl font-bold">Wie setzt sich der Score zusammen?</h2>
          <div>
            <button
              @click="togglePopup"
              class="p-1 bg-neutral-900 rounded-lg flex-grow-0"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 384 512"
                class="fill-white"
                height="32"
                width="32"
              >
                <path
                  d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"
                />
              </svg>
            </button>
          </div>
        </div>
        <p class="font-bold text-xl">Attribute</p>
        <ul>
          <li>Licht</li>
          <li>Temperatur</li>
          <li>Verkehr</li>
          <li>Wetter</li>
        </ul>
        <p class="font-bold text-xl pt-4">Berechnung</p>
        <p>a² + b² = c²</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showPopup: false, // Controls visibility of the popup
    };
  },
  methods: {
    togglePopup() {
      this.showPopup = !this.showPopup; // Toggle popup visibility
    },
  },
};
</script>
