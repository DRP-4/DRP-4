<script lang="ts">
import SpaceListItem from "./SpaceListItem.vue";
import { store as spacesStore } from "@/stores/spaces";
import { store as currentSpaceStore } from "@/stores/current_space";

export default {
  components: {
    SpaceListItem,
  },
  data() {
    return {
      spacesStore,
      currentSpaceStore,
    };
  },

  async mounted() {
    await spacesStore.loadFromDB();
  },
};
</script>

<template>
  <div class="h-100 w-100 card">
    <div class="card-header">Spaces</div>
    <div class="card-body p-3 overflow-y-auto">
      <ul class="list-group">
        <li
          :class="{
            'list-group-item': true,
            active: currentSpaceStore.spaceId === undefined,
            hstack: true,
          }"
        >
          <small><strong>Personal space</strong></small>
          <button
            v-if="currentSpaceStore.spaceId !== undefined"
            class="btn btn-sm btn-light flex-shrink-0 ms-auto"
            @click="currentSpaceStore.switchTo(undefined)"
          >
            Open
          </button>
        </li>
        <SpaceListItem
          v-for="space in spacesStore.sortedSpacesList()"
          :id="space.id"
          :key="space.id"
          :name="space.displayName"
          :is-owner="space.isOwned"
          :selected="currentSpaceStore.spaceId === space.id"
          @del="spacesStore.remove(space.id, 'del')"
          @leave="spacesStore.remove(space.id, 'leave')"
          @switch="currentSpaceStore.switchTo(space.id)"
        />
      </ul>
    </div>
  </div>
</template>
