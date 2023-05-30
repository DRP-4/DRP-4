<script lang="ts">
import type { Task } from "@/api";
import type { PropType } from "vue";

export default {
  props: {
    task: {
      type: Object as PropType<Task>,
      required: true,
    },
  },
};
</script>

<template>
  <div>
    <h1>Here's a task for you: {{ task.name }}</h1>
  </div>
</template>
