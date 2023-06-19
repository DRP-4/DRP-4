<script lang="ts">
import { store as timeJumpStore } from "@/stores/time_jump";

export default {
  data() {
    return {
      realDate: new Date(),
      currentDate: timeJumpStore.dateWithDebugOffset(),
      interval: undefined as ReturnType<typeof setInterval> | undefined,
      buttonDeltas: [5, 10, 15, 20, 30, 60, 120],
      timeJumpStore,
    };
  },

  async mounted() {
    this.interval = setInterval(() => {
      this.realDate = new Date();
      this.currentDate = timeJumpStore.dateWithDebugOffset();
    });
  },

  async unmounted() {
    clearInterval(this.interval);
  },
};
</script>

<template>
  <div class="vh-100 vw-100 p-4 d-flex">
    <div class="card m-auto h-auto">
      <div class="card-header hstack">
        <span class="me-auto"
          >Real time: {{ realDate.toTimeString().slice(0, 8) }}</span
        >
        <span>Mock time: {{ currentDate.toTimeString().slice(0, 8) }}</span>
        <span class="ms-auto"
          >Delta: {{ Math.floor(timeJumpStore.deltaInSeconds / 60) }} mins</span
        >
      </div>
      <div class="card-body">
        <div class="hstack">
          <button
            class="btn btn-sm btn-danger mx-1"
            @click="timeJumpStore.reset()"
          >
            Reset counter
          </button>
          <button
            v-for="delta in buttonDeltas"
            :key="delta"
            class="btn btn-sm btn-warning mx-1"
            @click="timeJumpStore.jump(delta * 60)"
          >
            + {{ delta }} min
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
