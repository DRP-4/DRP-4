<template>
  <div class="about">
    <h1>This is an about page</h1>
    <p>The counter value is {{ st.count }}</p>

    fds
  </div>
</template>

<script lang="ts">
import { store } from "../stores/counter";

export default {
  data() {
    return { st: store };
  },
};
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
