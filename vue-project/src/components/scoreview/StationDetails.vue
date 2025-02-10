
<!-- Station & line details -->
<template>
  <div class="flex flex-col items-center gap-1 font-bold text-white text-center">
    <div class="text-3xl font-extrabold bg-clip-text text-neutral-100 mb-3">
      {{ metadata.name }}
    </div>
    <div class="text-2xl font-bold text-white mb-1 bg-neutral-800 px-4 py-2 rounded-lg inline-block">
      {{ metadata.line }}
    </div>
    <div class="text-lg text-neutral-200 italic">
      {{ metadata.headsign }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    metadata: {
      type: Object,
      required: true,
    },
  },
};
</script>
