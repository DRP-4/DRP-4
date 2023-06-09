<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<script lang="ts">
import { store } from "../stores/time_jump";

export default {
  data() {
    return { st: store };
  },
};
</script>
