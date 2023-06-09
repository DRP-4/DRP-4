<script lang="ts">
import { Duration } from "@/api/duration";
import { newSession } from "@/api/session";

export default {
  data() {
    return {
      duration: "60",
    };
  },

  computed: {
    durationHumanized() {
      const duration = parseInt(this.duration);
      return new Duration(duration).humanized();
    },
  },

  methods: {
    async createSession() {
      await newSession(parseInt(this.duration));
      this.$emit("done");
    },
  },

  emits: ["done"],
};
</script>

<template>
  <div class="w-100 h-100 card">
    <div class="m-auto w-50 h-auto card">
      <div class="card-header">Create a new session</div>
      <div class="card-body">
        <div class="mb-3">
          <label for="duration" class="form-label"
            >Study Session Duration (with breaks):
            {{ durationHumanized }}</label
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
        <div class="hstack">
          <button
            type="button"
            class="btn btn-sm btn-success ms-1"
            @click="createSession"
          >
            Create session
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
