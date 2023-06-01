<script lang="ts">
import { getTasks, type Task, addTask } from "@/api";
import TaskItem from "../components/TaskItem.vue";

interface Model {
  tasks: Task[] | null;
  new_task: string;
}

export default {
  components: { TaskItem },
  data(): Model {
    return {
      tasks: null,
      new_task: "",
    };
  },
  mounted() {
    this.fetchTasks();
  },
  methods: {
    addTask() {
      const task = { name: this.new_task };
      addTask(task).then(() => {
        this.fetchTasks();
      })
    },

    fetchTasks() {
      getTasks().then((tasks) => {
        this.tasks = tasks;
      });
    },
  },
};
</script>

<template>
  <div v-if="tasks">
    <h2>We have the tasks!</h2>

    <ul>
      <div v-for="task in tasks" :key="task.id">
        <TaskItem :task="task" />
      </div>
    </ul>
  </div>
  <div v-else>Loading...</div>

  <input v-model="new_task" placeholder="Title" />
  <button @click="addTask()">Add Task</button>
</template>
