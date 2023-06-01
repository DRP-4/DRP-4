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
  <li>
    {{ task.name }}
  </li>
</template>
