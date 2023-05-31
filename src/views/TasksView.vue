<script lang="ts">
import { getTasks, type Task as Task } from "@/api";
import TaskItem from "../components/TaskItem.vue";

interface Model {
  tasks: Task[] | null;
  count: number;
}

export default {
  components: { TaskItem },
  data(): Model {
    return {
      count: 0,
      tasks: null,
    };
  },
  mounted() {
    getTasks().then((tasks) => {
      this.tasks = tasks;
    });
  },
  methods: {
    incr() {
      this.count++;
    },
  },
};
</script>

<template>
  <button @click="incr">count is: {{ count }}</button>
  <input v-model="count" type="range" min="0" max="10" />

  <div v-if="tasks">
    We have the tasks!

    <div v-for="task in tasks" :key="task.id">
      <TaskItem :task="task" />
    </div>
  </div>
  <div v-else>Loading...</div>
</template>
