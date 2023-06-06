<script lang="ts">
import { RouterLink } from "vue-router";

import type { Task } from "@/api/tasks";
import * as api from "@/api/tasks";

interface Data {
  duration: string; // DOM fuckery means this can't be a number
  tasks: Task[];
  pendingTask: string;
}

export default {
  components: { RouterLink },
  data(): Data {
    return {
      duration: "60",
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
    hasTasks(): boolean {
      return this.tasks.length != 0;
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
    newSession() {
      // api.newSession(
      //   this.tasks.map((t) => t.name),
      //   parseInt(this.duration)
      // );

      this.$router.push("/session");
    },
  },
};
</script>
<template>
  <div class="vh-100 d-flex align-items-center">
    <div class="card m-auto" style="width: 30rem">
      <div class="card-body">
        <div class="mb-3">
          <label for="duration" class="form-label"
            >Session Duration: {{ durationHumanized }}</label
          >
          <input
            v-model="duration"
            class="form-range"
            type="range"
            min="20"
            max="300"
            step="5"
          />
        </div>

        <div class="card mb-5">
          <div class="card-header">Tasks</div>
          <ul class="list-group list-group-flush">
            <li v-for="task in tasks" :key="task.id" class="list-group-item">
              {{ task.name }}
            </li>

            <!-- Place in form so focusing on the input binds enter to the button -->
            <li class="list-group-item">
              <form class="row" @submit.prevent>
                <div class="col-auto">
                  <input
                    v-model="pendingTask"
                    class="form-control"
                    type="text"
                    placeholder="New task..."
                  />
                </div>
                <div class="col-auto">
                  <button
                    :disabled="!pendingTask"
                    class="btn btn-primary"
                    @click="addTask()"
                  >
                    Add task
                  </button>
                </div>
              </form>
            </li>
          </ul>
        </div>

        <div class="d-flex">
          <button
            v-if="hasTasks"
            class="btn btn-outline-success btn-lg mx-auto"
            @click="newSession()"
          >
            Start Session!
          </button>

          <button v-else disabled="true" class="btn btn-lg mx-auto">
            Add some tasks!
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
