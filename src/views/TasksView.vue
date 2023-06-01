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
  <div v-if="tasks">
    <h2>We have the tasks!</h2>

    <div v-for="task in tasks" :key="task.id">
      <TaskItem :task="task" />
    </div>
  </div>
  <div v-else>Loading...</div>
</template>
