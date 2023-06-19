<script lang="ts">
import { endSession, giveFeedback } from "@/api/session";
import { store as timeJumpStore } from "@/stores/time_jump";
import { store as sessionStore } from "@/stores/session";
import { store as tasksStore } from "@/stores/tasks";
import { type Slot } from "@/api/session";
import TimelineElem from "./TimelineElem.vue";
import PostSessionFeedback from "@/components/PostSessionFeedback.vue";

import Satisfied from "@/components/icons/SatisfiedFace.vue";
import Neutral from "@/components/icons/NeutralFace.vue";
import Dissatisfied from "@/components/icons/DissatisfiedFace.vue";

export default {
  components: {
    TimelineElem,
    PostSessionFeedback,
    Satisfied,
    Neutral,
    Dissatisfied,
  },

  emits: ["done"],
  data() {
    return {
      sessionStore,
      currentDate: timeJumpStore.dateWithDebugOffset(),
      interval: undefined as ReturnType<typeof setInterval> | undefined,

      calculateSlotHeight(slot: Slot): number {
        const { start, end } = slot;
        if (sessionStore.session === undefined) {
          return 10;
        }
        const slotStart = start.getTime();
        const slotEnd = end.getTime();

        // TODO: This isn't right when `slot.completed_tasks.length` is >~5, but who does
        // 7 tasks in a session.
        return (
          Math.log2((slotEnd - slotStart) / 60000) * 2 +
          slot.completed_tasks.length * 2
        );
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

  async mounted() {
    await sessionStore.loadFromDB();
    this.interval = setInterval(() => {
      this.currentDate = timeJumpStore.dateWithDebugOffset();
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

    async slotFeedback(slot_id: number, feedback: number) {
      await giveFeedback(slot_id, feedback);
      await sessionStore.loadFromDB();
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
      <button
        type="button"
        class="btn btn-sm btn-danger ms-1"
        @click="endSession"
      >
        End session
      </button>
    </div>
    <div class="card-body overflow-y-scroll overflow-x-visible">
      <TimelineElem
        v-for="(slot, index) in sessionStore.session?.slots"
        :key="slot.slot_id"
        :starting-time="slot.start"
        :is-work="slot.is_work.valueOf()"
        :height="calculateSlotHeight(slot)"
        :completeness="calculateSlotCompleteness(slot.start, slot.end)"
      >
        <div v-if="slot.is_work" class="vstack h-100">
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

          <div class="mt-auto hstack">
            <div v-if="slot.end <= currentDate" class="mt-auto">
              <button
                type="button"
                class="btn btn-sm btn-primary"
                data-bs-toggle="modal"
                :data-bs-target="'#reviewbutt_' + (index / 2 + 1)"
              >
                Review Session {{ index / 2 + 1 }}
              </button>
              <div
                :id="'reviewbutt_' + (index / 2 + 1)"
                class="modal fade"
                tabindex="-1"
                role="dialog"
                aria-hidden="true"
              >
                <PostSessionFeedback
                  :name="(index / 2 + 1).toString()"
                  @satisfied="slotFeedback(slot.slot_id, 1)"
                  @neutral="slotFeedback(slot.slot_id, 2)"
                  @dissatisfied="slotFeedback(slot.slot_id, 3)"
                />
              </div>
            </div>
            <div class="ms-auto">
              <div v-if="slot.feedback == 1" class="emotions">
                <Satisfied />
              </div>
              <div v-if="slot.feedback == 2" class="emotions"><Neutral /></div>
              <div v-if="slot.feedback == 3" class="emotions">
                <Dissatisfied />
              </div>
            </div>
          </div>
        </div>
        <div v-else>Break</div>
      </TimelineElem>
    </div>
  </div>
</template>
