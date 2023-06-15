<script lang="ts">
import TaskListItem from "./TaskListItem.vue";
import NewTaskSetup from "./NewTaskSetup.vue";
import MagicUrl from "quill-magic-url";
import { type TaskID } from "@/api/tasks";
import { store as sessionStore } from "@/stores/session";
import { store as tasksStore } from "@/stores/tasks";

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
      selectedId: undefined,
      tasksStore,
      MagicUrl,
    };
  },

  created() {
    tasksStore.loadFromDB();
  },

  mounted() {
    const addTaskModal = this.$refs.addTaskModal as HTMLElement;
    const newTaskSetup = this.$refs.nts as HTMLInputElement;
    addTaskModal.addEventListener("shown.bs.modal", () => {
      // Technicly this type is wrong, but it works because we're calling the vue method
      // from the `methods` section, and ts thinks we're calling the `HTMLElement` method,
      // but it's probably fine.
      newTaskSetup.focus();
    });
  },

  methods: {
    async remove(id: TaskID) {
      await tasksStore.remove(id);
      await sessionStore.loadFromDB();
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
        ref="addTaskModal"
        class="modal fade"
        tabindex="-1"
        role="dialog"
        aria-labelledby="addNewTaskLabel"
        aria-hidden="true"
      >
        <NewTaskSetup ref="nts" @add="(newTask) => tasksStore.add(newTask)" />
      </div>
    </div>

    <div class="card-body overflow-y-scroll overflow-x-visible">
      <div
        v-for="task in tasksStore.sortedTasksList()"
        :key="task.id"
        class="p-2"
      >
        <TaskListItem
          :task="task"
          :in-session="inSession"
          @task:update="(newTask) => tasksStore.update(newTask)"
          @delete="remove(task.id)"
        />
      </div>
    </div>
  </div>
</template>
