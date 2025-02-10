
<!-- Popup for the score explanation -->
<template>
  <div class="fixed inset-0 bg-black bg-opacity-50">
    <div class="bg-neutral-800 text-neutral-200 p-8 rounded-lg shadow-lg w-full">
      <div class="flex justify-between">

        <!-- Popup title -->
        <h2 class="text-xl font-bold">
          Wie setzten sich die Scores zusammen?
        </h2>

        <!-- Close button -->
        <div>
          <button @click="closePopup" class="p-1 bg-neutral-900 rounded-lg flex-grow-0">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" class="fill-white" height="32" width="32">
              <path
                d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z" />
            </svg>
          </button>
        </div>

      </div>

      <!-- Content of the popup  -->
      <ScoreExplanationContent />

    </div>
  </div>
</template>

<script>
import ScoreExplanationContent from './ScoreExplanationContent.vue';

export default {
  components: {
    ScoreExplanationContent,
  },
  methods: {
    closePopup() {
      this.$emit('close');
    },

  },
};
</script>