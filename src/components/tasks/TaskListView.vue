<script lang="ts">
import TaskListItem from "./TaskListItem.vue";
import NewTaskSetup from "./NewTaskSetup.vue";
import MagicUrl from "quill-magic-url";
import { tasks, deleteTask, Task, type TaskID } from "@/api/tasks";
import { createTask } from "@/api/tasks";

export default {
  components: {
    TaskListItem,
    NewTaskSetup,
  },
  props: {
    inSession: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      modalKey: 0,
      tasks: new Map(),
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

  async created() {
    this.tasks = await tasks();
  },

  methods: {
    async add(newTask: { name: string; description?: string }) {
      const id = await createTask(newTask);
      this.tasks.set(
        id,
        new Task(id, newTask.name, { description: newTask.description })
      );
    },

    update(task: Task) {
      this.tasks.set(task.id, task);
    },

    remove(id: TaskID) {
      this.tasks.delete(id);
      deleteTask(id);
    },
  },
};
</script>

<template>
  <div class="card h-100 w-100">
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
        <NewTaskSetup @add="add" />
      </div>
    </div>
    <div class="card-body overflow-y-scroll overflow-x-visible">
      <div v-for="task in sortedTaskList" :key="task.id" class="p-2">
        <TaskListItem
          :task="task"
          :in-session="inSession"
          @task:update="(newTask) => update(newTask)"
          @delete="remove(task.id)"
        />
      </div>
    </div>
  </div>
</template>
