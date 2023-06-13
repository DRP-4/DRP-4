<script lang="ts">
import { jumpSeconds, resetJumpCounter } from "@/api/debug";
import { type Session, getSession, endSession } from "@/api/session";
import { store } from "@/stores/time_jump";
import TimelineElem from "./TimelineElem.vue";

function dateWithDebugOffset() {
  const thisInstant = new Date();
  const thisInstantUnix = thisInstant.getTime();
  const newInstantUnix = thisInstantUnix + store.deltaInSeconds * 1000;
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
      session: undefined as Session | undefined,
      currentDate: dateWithDebugOffset(),
      interval: undefined as ReturnType<typeof setInterval> | undefined,

      calculateSlotHeight(start: Date, end: Date): string {
        if (this.session === undefined) {
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
    this.session = await getSession();
    this.interval = setInterval(() => {
      this.currentDate = dateWithDebugOffset();
      if (this.session !== undefined) {
        if (this.currentDate > this.session?.end) {
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
      endSession();
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
        >Session (in progress, current time
        {{ currentDate.toTimeString() }})</span
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
    <div class="card-body overflow-hidden">
      <!-- TODO: what should the key for the slot be? -->
      <TimelineElem
        v-for="slot in session?.slots"
        :key="slot.start.getTime()"
        :starting-time="slot.start"
        :is-work="slot.is_work.valueOf()"
        :height="calculateSlotHeight(slot.start, slot.end)"
        :completeness="calculateSlotCompleteness(slot.start, slot.end)"
      >
        <small>{{ slot.is_work ? "Study slot" : "Break" }}</small>
      </TimelineElem>
    </div>
  </div>
</template>
