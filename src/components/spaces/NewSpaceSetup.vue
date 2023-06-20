<script lang="ts">
import { store as spacesStore } from "@/stores/spaces";

export default {
  data() {
    return {
      displayName: "",
    };
  },

  methods: {
    add() {
      spacesStore.add(this.displayName);
    },
  },
};
</script>

<template>
  <div class="h-auto w-100 card">
    <div class="card-header">Create a new work space</div>
    <div class="card-body">
      <div class="input-group input-group-sm">
        <input
          v-model="displayName"
          type="text"
          class="form-control"
          placeholder="Display name"
        />
        <div class=""></div>
        <button
          class="input-group-append btn btn-success"
          :disabled="displayName.length == 0"
          @click="add"
        >
          Create
        </button>
      </div>
    </div>
  </div>
</template>
