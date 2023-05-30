<script lang="ts">
import { getTasks, type Task as TaskT } from "@/api";
import Task from "../components/Task.vue";

interface Model {
  tasks: TaskT[] | null;
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
  components: {
    Task,
  },
};
</script>

<template>
  <button @click="incr">count is: {{ count }}</button>
  <input type="range" min="0" max="10" v-model="count" />

  <div v-if="tasks">
    We have the tasks!

    <div v-for="task in tasks">
      <Task :task="task" />
    </div>
  </div>
  <div v-else>Loading...</div>
</template>
