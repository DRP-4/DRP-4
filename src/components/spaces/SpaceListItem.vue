<script lang="ts">
function inviteLink(id: string): string {
  const url = new URL(window.location.origin);
  url.searchParams.append("join", id);
  return url.href;
}

export default {
  props: {
    id: {
      type: String,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    selected: {
      type: Boolean,
      required: true,
    },
    isOwner: {
      type: Boolean,
      required: true,
    },
  },

  emits: ["switch", "del", "leave"],

  methods: {
    copy() {
      navigator.clipboard.writeText(inviteLink(this.id));
    },
  },
};
</script>

<template>
  <li :class="{ 'list-group-item': true, active: selected }">
    <div class="hstack">
      <small class="align-middle me-2 flex-shrink-0">{{ name }}</small>
      <span
        class="text-muted ms-auto me-3 flex-shrink-1 text-nowrap overflow-hidden"
        style="font-family: monospace; min-width: 0"
        ><small>#{{ id }}</small></span
      >
      <div class="btn-group flex-shrink-0">
        <button class="btn btn-sm btn-light" @click="copy">Copy invite</button>
        <button
          v-if="!selected"
          class="btn btn-sm btn-light"
          @click="$emit('switch')"
        >
          Switch to
        </button>
        <button
          v-if="isOwner"
          class="btn btn-sm btn-danger"
          @click="$emit('del')"
        >
          Delete
        </button>
        <button v-else class="btn btn-sm btn-danger" @click="$emit('leave')">
          Leave
        </button>
      </div>
    </div>
  </li>
</template>
