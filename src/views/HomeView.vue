<script lang="ts">
import type { Task } from "@/api/tasks";
import * as api from "@/api/tasks";

interface Data {
  duration: string; // DOM fuckery means this can't be a number
  tasks: Task[];
  pendingTask: string;
}

export default {
  data(): Data {
    return {
      duration: "30",
      pendingTask: "",
      tasks: [],
    };
  },
  computed: {
    durationHumanized() {
      const duration = parseInt(this.duration);

      if (duration < 60) {
        return `${duration} mins`;
      } else if (duration === 60) {
        return "1 hour";
      } else {
        const hours = Math.floor(duration / 60);
        const minutes = duration % 60;

        if (minutes === 0) {
          return `${hours} hours`;
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
    startSession() {
      api.startSession(
        this.tasks.map((t) => t.name),
        parseInt(this.duration)
      );
    },
  },
};
</script>
<template>
  <div class="d-flex vh-100">
    <main class="m-auto">
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

      <!-- Place in form so focusing on the input binds enter to the button -->
      <form>
        <input
          v-model="pendingTask"
          type="text"
          placeholder="What needs doing?"
        />
        <button :disabled="!pendingTask" @click="addTask()">Add task</button>
      </form>

      <p class="startwrap">
        <button class="start" @click="startSession()">Start Now!</button>
      </p>
    </main>
  </div>
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
