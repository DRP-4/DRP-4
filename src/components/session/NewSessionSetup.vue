<script lang="ts">
import { Duration } from "@/api/duration";
import { newSession, getSession } from "@/api/session";

export default {
  emits: ["done"],
  data() {
    return {
      duration: "60",
      savedSession: false,
    };
  },

  computed: {
    durationHumanized() {
      const duration = parseInt(this.duration);
      return new Duration(duration).humanized();
    },
  },

  mounted(this): void {
    // if get session fails with a 404, there is no previous session in the DB
    // for us to load settings from
    getSession().then(
      () => {
        this.savedSession = true;
      },
      () => {
        this.savedSession = false;
      }
    );
  },

  methods: {
    async createSession() {
      await newSession(parseInt(this.duration));
      this.$emit("done");
    },
  },
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
            class="btn btn-sm btn-outline-success ms-1"
            @click="createSession"
          >
            Create session
          </button>
          <button
            v-if="savedSession"
            type="button"
            class="btn btn-sm btn-success ms-1"
            @click="restoreSession"
          >
            Restore session
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
