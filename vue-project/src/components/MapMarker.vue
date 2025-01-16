<template>
  <div class="my-component bg-pink-600">
    <h1>{{ title }}</h1>
    <p>This is a simple Vue component.</p>
    <button @click="handleClick">Click me</button>
  </div>
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
