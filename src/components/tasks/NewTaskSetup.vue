<script lang="ts">
import { QuillEditor } from "@vueup/vue-quill";
import MagicUrl from "quill-magic-url";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

export default {
  components: {
    QuillEditor,
  },

  emits: ["add"],

  data() {
    return {
      taskName: "",
      taskDescription: "",
      includeDescription: false,
      MagicUrl,
    };
  },

  methods: {
    add() {
      if (this.taskName.trim().length == 0) {
        return;
      }
      this.$emit("add", {
        name: this.taskName,
        description: this.includeDescription ? this.taskDescription : undefined,
      });
      this.reset();
    },

    reset() {
      this.taskName = "";
      this.taskDescription = "";
      this.includeDescription = false;
    },

    focus() {
      const el = this.$refs.newTaskName as HTMLInputElement;
      el.focus();
    },
  },
};
</script>

<template>
  <div class="modal-dialog modal-dialog-centered" role="document">
    <form class="modal-content" onsubmit="return false;">
      <div class="modal-header">
        <h5 id="addNewTaskLabel" class="modal-title">Add new task</h5>
        <button
          type="button"
          class="close btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
          @click="reset"
        ></button>
      </div>
      <div class="modal-body">
        <div class="mb-3">
          <input
            ref="newTaskName"
            v-model="taskName"
            type="text"
            :class="{
              'form-control': true,
              'w-100': true,
            }"
            placeholder="Task name (required)"
          />
        </div>
        <div class="card">
          <div class="card-header">
            <div class="form-check">
              <input
                id="includeDescription"
                v-model="includeDescription"
                class="form-check-input"
                type="checkbox"
              />
              <label class="form-check-label" for="includeDescription"
                >Add description
                <span class="text-muted">(optional)</span></label
              >
            </div>
          </div>
          <div v-if="includeDescription" class="card-body p-1">
            <QuillEditor
              v-model:content="taskDescription"
              theme="snow"
              toolbar="essential"
              content-type="html"
              :modules="{
                name: 'Magic URL plugin',
                module: MagicUrl,
              }"
            />
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button
          type="button"
          class="btn btn-secondary"
          data-bs-dismiss="modal"
          @click="reset"
        >
          Close
        </button>
        <button
          type="submit"
          class="btn btn-success"
          data-bs-dismiss="modal"
          :disabled="taskName.trim().length == 0"
          @click="add"
        >
          Add new task
        </button>
      </div>
    </form>
  </div>
</template>
