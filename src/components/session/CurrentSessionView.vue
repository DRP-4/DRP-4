<script lang="ts">
import { jumpSeconds, resetJumpCounter } from "@/api/debug";
import { endSession } from "@/api/session";
import { store as timeJumpStore } from "@/stores/time_jump";
import { store as sessionStore } from "@/stores/session";
import { store as tasksStore } from "@/stores/tasks";
import TimelineElem from "./TimelineElem.vue";

function dateWithDebugOffset() {
  const thisInstant = new Date();
  const thisInstantUnix = thisInstant.getTime();
  const newInstantUnix = thisInstantUnix + timeJumpStore.deltaInSeconds * 1000;
  const newInstant = new Date(newInstantUnix);
  return newInstant;
}

export default {
  components: {
    TimelineElem,
  },

  emits: ["done"],
  data() {
    return {
      sessionStore,
      currentDate: dateWithDebugOffset(),
      interval: undefined as ReturnType<typeof setInterval> | undefined,

      calculateSlotHeight(start: Date, end: Date): string {
        if (sessionStore.session === undefined) {
          return "auto";
        }
        const slotStart = start.getTime();
        const slotEnd = end.getTime();

        return `${Math.log2((slotEnd - slotStart) / 60000) * 2}em`;
      },

      calculateSlotCompleteness(start: Date, end: Date): number {
        const slotStart = start.getTime();
        const slotEnd = end.getTime();
        const current = this.currentDate.getTime();
        const ratio = (current - slotStart) / (slotEnd - slotStart);
        return Math.min(Math.max(ratio, 0.0), 1.0);
      },

      isInProgress(start: Date, end: Date): boolean {
        return start <= this.currentDate && this.currentDate <= end;
      },

      isAhead(start: Date): boolean {
        return this.currentDate <= start;
      },
    };
  },

  async created() {
    await resetJumpCounter();
  },

  async mounted() {
    await sessionStore.loadFromDB();
    this.interval = setInterval(() => {
      this.currentDate = dateWithDebugOffset();
      if (this.sessionStore.session !== undefined) {
        if (this.currentDate > this.sessionStore.session?.end) {
          endSession();
          this.$emit("done");
        }
      }
    }, 100);
  },

  async unmounted() {
    clearInterval(this.interval);
  },

  methods: {
    async endSession() {
      await sessionStore.endSession();
      await tasksStore.loadFromDB();
      this.$emit("done");
    },

    async jump() {
      const JUMPING_BY = 900; // 15 minutes
      await jumpSeconds(JUMPING_BY);
    },
  },
};
</script>

<template>
  <div class="w-100 h-100 card">
    <div class="card-header hstack">
      <span class="me-auto"
        >Session (Time is {{ currentDate.toLocaleTimeString("en-GB") }})</span
      >
      <button type="button" class="btn btn-sm btn-warning me-1" @click="jump">
        Skip 15 minutes ahead
      </button>
      <button
        type="button"
        class="btn btn-sm btn-danger ms-1"
        @click="endSession"
      >
        End session
      </button>
    </div>
    <div class="card-body overflow-y-scroll overflow-x-visible">
      <!-- TODO: what should the key for the slot be? -->
      <TimelineElem
        v-for="slot in sessionStore.session?.slots"
        :key="slot.start.getTime()"
        :starting-time="slot.start"
        :is-work="slot.is_work.valueOf()"
        :height="calculateSlotHeight(slot.start, slot.end)"
        :completeness="calculateSlotCompleteness(slot.start, slot.end)"
      >
        <div v-if="slot.is_work" class="vstack">
          <h6 class="mb-1">Study slot</h6>
          <small v-if="slot.completed_tasks.length > 0" class="mb-2 text-muted"
            >Tasks completed</small
          >
          <ul
            v-if="slot.completed_tasks.length > 0"
            class="list-group list-group-sm"
          >
            <li
              v-for="task in slot.completed_tasks"
              :key="task.name"
              class="list-group-item"
            >
              <small>{{ task.name }}</small>
            </li>
          </ul>
        </div>
        <div v-else>Break</div>
      </TimelineElem>
    </div>
  </div>
</template>
