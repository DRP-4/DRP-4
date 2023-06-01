<script lang="ts">
import { store } from "../stores/counter";

export default {
  data() {
    return { store };
  },
};
</script>

<template>
  <h1>The Count is {{ store.count }}</h1>

  <button @click="store.increment()">Increment</button>
</template>
