<script lang="ts">
import { getTasks, type Task as Task } from "@/api";
import TaskItem from "../components/TaskItem.vue";

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
  components: { TaskItem },
};
</script>

<template>
  <button @click="incr">count is: {{ count }}</button>
  <input type="range" min="0" max="10" v-model="count" />

  <div v-if="tasks">
    We have the tasks!

    <div v-for="task in tasks" :key="task.id">
      <TaskItem :task="task" />
    </div>
  </div>
  <div v-else>Loading...</div>
</template>
