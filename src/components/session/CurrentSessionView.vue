<script lang="ts">
import { type Session, getSession, endSession } from "@/api/session";
import TimelineElem from "./TimelineElem.vue";

export default {
  data() {
    return {
      session: undefined as Session | undefined,
      currentDate: new Date(),

      calculateSlotHeight(start: Date, end: Date): string {
        if (this.session === undefined) {
          return "auto";
        }
        console.log(this.session);
        const sessionStart = Math.floor(this.session.start.getTime() / 1000);
        const sessionEnd = Math.floor(this.session.end.getTime() / 1000);
        const slotStart = Math.floor(start.getTime() / 1000);
        const slotEnd =Math.floor(end.getTime() / 1000);

        const ratio = (slotEnd - slotStart) / (sessionEnd - sessionStart);
        console.log(ratio, sessionEnd, sessionStart, slotEnd, slotStart);
        return `${100 * ratio}%`;
      },

      isInProgress(start: Date, end: Date): boolean {
        return start <= this.currentDate && this.currentDate <= end;
      },

      isAhead(start: Date): boolean {
        return this.currentDate <= start;
      }
    };
  },

  async created() {
    this.session = await getSession();
    const self = this;
    setInterval(() => {
      this.currentDate = new Date();

      if (this.session !== undefined) {
        if (this.currentDate > this.session?.end) {
          endSession();
          this.$emit("done");
        }
      }
    }, 100);
  },

  components: {
    TimelineElem,
  },

  methods: {
    async endSession() {
      endSession();
      this.$emit("done");
    },
  },

  emits: ["done"],
};
</script>

<template>
  <div class="w-100 h-100 card">
    <div class="card-header hstack">
      <span class="me-auto">Session (in progress)</span>
      <button type="button" class="btn btn-sm btn-warning me-1">
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
    <div class="card-body">
      <TimelineElem
        v-for="slot in session?.slots"
        :starting-time="slot.start"
        :is-work="slot.is_work.valueOf()"
        :height="calculateSlotHeight(slot.start, slot.end)"
        :in-progress="isInProgress(slot.start, slot.end)"
        :ahead="isAhead(slot.start)"
      >
      <small>{{ slot.is_work ? "Study slot" : "Break" }}</small>
      </TimelineElem>
    </div>
  </div>
</template>
