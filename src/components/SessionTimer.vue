<script lang="ts">
import session_mirror from "@/stores/session_mirror";

interface Slot {
  id: number;
  workId: number | null;
  startDate: Date;
  tasksCompleted: number;
  minutes: number;
}

interface Task {
  id: number;
  name: string;
  completed: boolean;
}

interface Model {
  prevSlots: Slot[];
  currentSlot: Slot;
  sessionMinutes: number;
  tasks: Task[];
  currentDate: Date;
}

function mkDate(time: string): Date {
  let times = time.split(":");
  let date = new Date();
  date.setHours(parseInt(times[0]));
  date.setMinutes(parseInt(times[1]));
  date.setSeconds(0);
  return date;
}

function loadTasks(): Task[] {
  return session_mirror.tasks_todo.map(({ id, name }) => {
    return { id, name, completed: false };
  });
}

export default {
  data(): Model {
    return {
      prevSlots: [
        {
          id: 1,
          startDate: mkDate("16:30"),
          minutes: 45,
          workId: 1,
          tasksCompleted: 2,
        },
        {
          id: 2,
          startDate: mkDate("17:15"),
          minutes: 15,
          workId: null,
          tasksCompleted: 0,
        },
        {
          id: 3,
          startDate: mkDate("17:30"),
          minutes: 45,
          workId: 2,
          tasksCompleted: 0,
        },
      ],
      currentSlot: {
        id: 4,
        startDate: mkDate("18:15"),
        minutes: 15,
        workId: null,
        tasksCompleted: 0,
      },
      sessionMinutes: session_mirror.duration_mins,
      tasks: loadTasks(),
      currentDate: new Date(),
    };
  },

  computed: {
    currentSessionHeight(): number {
      let res =
        (100 *
          (this.currentDate.getTime() - this.currentSlot.startDate.getTime())) /
        (60000 * this.sessionMinutes);
      console.log(res);
      return res;
    },
  },

  mounted: function () {
    let self = this;
    this.updateCurrentDate();

    setInterval(function () {
      self.updateCurrentDate();
    }, 100);
  },

  methods: {
    updateCurrentDate() {
      this.currentDate = new Date();
    },
  },
};
</script>

<template>
  <div class="d-flex vh-100 p-2 align-items-center justify-content-center">
    <div class="border bg-light w-100 h-100 d-flex flex-column">
      <!-- Slots timetable  -->
      <div class="column flex-grow-1 d-flex flex-column align-items-start">
        <div
          v-for="slot in prevSlots"
          :key="slot.id"
          :style="{ height: (100 * slot.minutes) / sessionMinutes + '%' }"
          class="d-flex flex-row w-100 align-items-center"
        >
          <div class="d-flex flex-column align-items-center h-100">
            <div class="small">
              {{ slot.startDate.toTimeString().slice(0, 5) }}
            </div>
            <div v-if="slot.workId" class="work"></div>
            <div v-else class="break"></div>
          </div>
          <div
            v-if="slot.workId"
            class="flex-grow-1 m-2 card h-auto p-2 container-fluid"
          >
            <div class="row">
              <div class="col-6">
                <u class="m-2">Study slot #{{ slot.workId }}</u>
                <div class="m-2">&#128337; {{ slot.minutes }}m</div>
                <div>
                  <div v-if="slot.tasksCompleted == 1" class="m-2">
                    &#x1F4DA; 1 tasks
                  </div>
                  <div v-else-if="slot.tasksCompleted" class="m-2">
                    &#x1F4DA; {{ slot.tasksCompleted }} tasks
                  </div>
                </div>
              </div>
              <div class="col-6"></div>
            </div>
          </div>
          <div v-else class="flex-grow-1 m-2 card p-2 d-flex">
            <p class="my-auto">Break: {{ slot.minutes }} minutes</p>
          </div>
        </div>

        <div
          :style="{
            height: currentSessionHeight + '%',
          }"
          class="d-flex flex-row w-100 align-items-center"
        >
          <div class="d-flex flex-column align-items-center h-100">
            <div class="small">
              {{ currentSlot.startDate.toTimeString().slice(0, 5) }}
            </div>
            <div v-if="currentSlot.workId" class="work"></div>
            <div v-else class="break"></div>
            <div class="small">
              {{ currentDate.toTimeString().slice(0, 5) }}
            </div>
          </div>
          <div
            v-if="currentSlot.workId"
            class="flex-grow-1 m-2 card h-auto p-2 container-fluid"
          >
            <div class="row">
              <div class="col-6">
                <u class="m-2"
                  >Study slot #{{ currentSlot.workId }}
                  <span class="text-muted">(in progress)</span></u
                >
                <div class="m-2">&#128337; {{ currentSlot.minutes }}m</div>
                <div>
                  <div v-if="currentSlot.tasksCompleted == 1" class="m-2">
                    &#x1F4DA; 1 tasks
                  </div>
                  <div v-else-if="currentSlot.tasksCompleted" class="m-2">
                    &#x1F4DA; {{ currentSlot.tasksCompleted }} tasks
                  </div>
                </div>
              </div>
              <div class="col-6"></div>
            </div>
          </div>
          <div v-else class="flex-grow-1 m-2 card p-2 d-flex">
            <p class="my-auto">
              Break <span class="text-muted">(in progress)</span>:
              {{ currentSlot.minutes }} minutes
            </p>
          </div>
        </div>
      </div>

      <!-- Tasks -->
      <div class="p-2">
        <ul class="w-95 m-auto list-group overflow-auto">
          <li
            v-for="task in tasks"
            :key="task.id"
            class="list-group-item"
            :class="{ 'list-group-item-success': task.completed }"
          >
            <div class="d-flex">
              <input
                :id="`task${task.id}`"
                v-model="task.completed"
                type="checkbox"
                class="form-check-input flex-shrink-0"
              />
              <label for="completed" class="form-check-label ms-2">{{
                task.name
              }}</label>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.h-95 {
  height: 95%;
}

.w-90 {
  width: 95%;
}

.work {
  width: 15px;
  border: 0px;
  border-radius: 5px;
  background-color: rgb(226, 111, 111);
  height: 100%;
}

.break {
  width: 15px;
  border: 0px;
  border-radius: 5px;
  background-color: rgb(112, 112, 216);
  height: 100%;
}
</style>
