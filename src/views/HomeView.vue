<script lang="ts">
import type { Task } from "@/api/tasks";

interface Data {
  duration: number; // DOM fuckery means this can also be string
  tasks: Task[];
  pendingTask: string;
}

export default {
  data(): Data {
    return {
      duration: 30,
      pendingTask: "",
      tasks: [],
    };
  },
  computed: {
    durationHumanized() {
      if (this.duration < 60) {
        return `${this.duration} mins`;
      } else if (this.duration == 60) {
        // This can't be ===, because lol
        return "1 hour";
      } else {
        const hours = Math.floor(this.duration / 60);
        const minutes = this.duration % 60;

        if (minutes === 0) {
          return `${hours} hours`;
        } else if (minutes === 30) {
          return `${hours}.5 hours`;
        } else {
          return `${hours} hours ${minutes} mins`;
        }
      }
    },
  },
  methods: {
    addTask() {
      const task = {
        name: this.pendingTask,
        id: this.tasks.length,
      };
      this.tasks.push(task);
      this.pendingTask = "";
    },
  },
};
</script>
<template>
  <main>
    <input
      v-model="duration"
      class="timeslider"
      type="range"
      min="5"
      max="120"
      step="5"
      list="tickmarks"
    />

    <datalist id="tickmarks">
      <option value="5"></option>
      <option value="15"></option>
      <option value="30"></option>
      <option value="60"></option>
      <option value="120"></option>
    </datalist>

    {{ durationHumanized }}

    <ol v-if="tasks.length">
      Things to study:
      <li v-for="task in tasks" :key="task.id">
        {{ task.name }}
      </li>
    </ol>
    <div v-else>No Task Yet!</div>

    <input v-model="pendingTask" type="text" placeholder="What needs doing?" />

    <button :disabled="!pendingTask" @click="addTask()">Add task</button>

    <p class="startwrap">
      <button class="start">Start Now!</button>
    </p>
  </main>
</template>

<style scoped>
.timeslider {
  width: 100%;
}

main {
  margin-top: 5em;
}

datalist {
  display: flex;
  justify-content: space-between;
  color: red;
}

.startwrap {
  display: flex;
  justify-content: center;
  margin-top: 5em;
}

.start {
  width: 40em;
  height: 3em;
}
</style>
