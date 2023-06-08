<script lang="ts">
import TaskListItem from "./TaskListItem.vue";
import NewTaskSetup from "./NewTaskSetup.vue";
import MagicUrl from "quill-magic-url";
import { Task, type TaskID } from "@/api/tasks";
import { Duration } from "@/api/duration";

export default {
  components: {
    TaskListItem,
    NewTaskSetup,
  },
  data() {
    return {
      modalKey: 0,
      tasks: new Map([
        [1, new Task(1, "Clean the room").withTimeEstimate(new Duration(15))],
        [
          2,
          new Task(2, "Study probability").withTimeEstimate(new Duration(30)),
        ],
        [3, new Task(3, "Study vectors").withTimeEstimate(new Duration(45))],
        [
          4,
          new Task(4, "Book tickets to Cambridge").withDescription(
            "Here is a sample task description"
          ),
        ],
      ]),
      selectedId: undefined,
      console,
      MagicUrl,
    };
  },

  computed: {
    sortedTaskList(): Task[] {
      return [...this.tasks.values()].sort((l, r) => l.id - r.id);
    },
  },

  methods: {
    update(task: Task) {
      this.tasks.set(task.id, task);
    },

    remove(id: TaskID) {
      this.tasks.delete(id);
    },
  },
};
</script>

<template>
  <div class="card h-100 w-100 overflow-scroll">
    <div class="card-header hstack">
      <span class="me-auto">Tasks</span>

      <!-- Add new task modal -->
      <button
        type="button"
        class="btn btn-sm btn-primary"
        data-bs-toggle="modal"
        data-bs-target="#addTaskModal"
      >
        Add new task
      </button>
      <div
        id="addTaskModal"
        class="modal fade"
        tabindex="-1"
        role="dialog"
        aria-labelledby="addNewTaskLabel"
        aria-hidden="true"
      >
        <NewTaskSetup />
      </div>
    </div>
    <div class="card-body">
      <div v-for="task in sortedTaskList" :key="task.id" class="p-2">
        <TaskListItem
          :task="task"
          @task:update="(newTask) => update(newTask)"
          @delete="remove(task.id)"
        />
      </div>
    </div>
  </div>
</template>
