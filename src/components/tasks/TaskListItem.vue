<script lang="ts">
import { Task, updateTask } from "@/api/tasks";
import { QuillEditor } from "@vueup/vue-quill";
import MagicUrl from "quill-magic-url";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

export default {
  components: {
    QuillEditor,
  },

  props: {
    task: {
      type: Task,
      required: true,
    },
    inSession: {
      type: Boolean,
      required: true,
    }
  },

  emits: ["delete", "task:update"],
  data() {
    return {
      editedName: this.task.name,
      editedDescription: undefined as string | undefined,
      MagicUrl,
    };
  },

  methods: {
    updateName(event: Event) {
      const target = event.target;
      if (target instanceof HTMLInputElement) {
        this.$emit("task:update", { ...this.task, name: target.value });
        updateTask({ id: this.task.id, name: target.value });
      }
    },

    saveDescription() {
      this.$emit("task:update", {
        ...this.task,
        description: this.editedDescription,
      });
      updateTask({ id: this.task.id, description: this.editedDescription });
      this.editedDescription = undefined;
    },

    complete(event: Event) {
      const target = event.target;
      if (target instanceof HTMLInputElement) {
        this.$emit("task:update", {
          ...this.task,
          complete: target.checked
        });
        updateTask({ id: this.task.id, complete: target.checked });
      }
    }
  },
};
</script>

<template>
  <div class="card">
    <!-- Card header (task name, delete button) -->
    <div class="card-header hstack">
      <div class="form-check" v-if="inSession">
        <input class="form-check-input" type="checkbox" :checked="task.complete" @input="complete">
      </div>
      <input
        ref="nameInput"
        v-model="editedName"
        :style="{
          'text-decoration': task.complete ? 'line-through' : 'none',
        }"
        class="name-input ms-auto"
        placeholder="Enter task name..."
        type="text"
        @blur="updateName"
      />
      <!-- Description edit status buttons -->
      <button
        v-if="task.description === undefined && editedDescription === undefined"
        type="button"
        class="btn btn-light btn-sm mx-3"
        style="white-space: nowrap"
        @click="editedDescription = ''"
      >
        Add description
      </button>
      <button
        v-else-if="editedDescription === undefined"
        type="button"
        class="btn btn-light btn-sm mx-3"
        style="white-space: nowrap"
        @click="editedDescription = task.description"
      >
        Edit description
      </button>
      <button
        v-else
        type="button"
        class="btn btn-success btn-sm mx-3"
        style="white-space: nowrap"
        @click="saveDescription"
      >
        Save description
      </button>

      <button
        type="button"
        class="btn-close"
        aria-label="Delete"
        @click="$emit('delete')"
      ></button>
    </div>
    <!-- Card body (task description) -->
    <div
      v-if="task.description !== undefined || editedDescription !== undefined"
      class="card-body p-0"
    >
      <QuillEditor
        v-if="editedDescription !== undefined"
        v-model:content="editedDescription"
        theme="snow"
        toolbar="essential"
        content-type="html"
        :modules="{
          name: 'Magic URL plugin',
          module: MagicUrl,
        }"
      />
      <QuillEditor
        v-else
        theme=""
        toolbar="none"
        content-type="html"
        :read-only="true"
        :content="task.description"
      />
    </div>
  </div>
</template>

<style scoped>
.task-name:focus {
  background-color: var(--bs-light);
}

.name-input {
  all: unset;
  /* Same effect as <small> */
  font-size: 0.875em;
  width: 100%;
}

.description-input {
  all: unset;
  /* Same effect as <small> */
  font-size: 0.875em;

  width: 100%;
  height: 100%;
}
</style>
