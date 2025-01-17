<template>
  <input
    class="bg-neutral-800 text-white p-2 rounded-xl"
    v-model="message"
    placeholder="Start"
  />
  <input
    class="bg-neutral-800 text-white p-2 rounded-xl"
    v-model="message"
    placeholder="AAAAAAAAAAAAAAAaaaa"
  />
</template>

<script>
export default {
  name: "MyComponent", // Component name
  props: {
    title: {
      type: String,
      required: true,
    },
  },
  methods: {
    handleClick() {
      alert("Button clicked!");
    },
  },
};
</script>
