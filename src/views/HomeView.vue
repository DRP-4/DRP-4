<script  lang="ts">
import CounterClicker from "../components/CounterClicker.vue";
import type { Task } from "@/api";

interface Data {
  duration: number; // DOM fuckery means this can also be string
  tasks: Task[];
  pendingTask: string
}

export default {
  components: { CounterClicker },
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
      } else if (this.duration == 60) { // This can't be ===, because lol
        return "1 hour";
      } else {
        const hours = Math.floor(this.duration / 60);
        const minutes = this.duration % 60;

        if (minutes === 0) {
          return `${hours} hours`;
        } else if (minutes === 30) {
          return `${hours}.5 hours`
        } else {
          return `${hours} hours ${minutes} mins`;
        }
      }
    }
  },
  methods: {
    addTask() {
      const task = {
        name: this.pendingTask,
        id: this.tasks.length
      };
      this.tasks.push(task);
      this.pendingTask = "";
    }
  }
};
</script>

<template>
  <main>
    <CounterClicker />
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
