<template>
  <!-- make this button work -->
  <button @click="incr">count is: {{ count }}</button>
  <input type="range" min="0" max="10" v-model="count" />

  <div v-if="tasks">We have the tasks!</div>
  <div v-else>Loading...</div>
</template>

<script lang="ts">
import { getTasks, type Task } from "@/api";

interface Model {
  tasks: Task[] | null;
  count: number;
}

export default {
  data(): Model {
    return {
      count: 0,
      tasks: null,
    };
  },
  methods: {
    incr() {
      this.count++;
    },
  },
  mounted() {
    getTasks().then((tasks) => {
      this.tasks = tasks;
    });
  },
};
</script>
