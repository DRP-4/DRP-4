<script lang="ts">
import TaskListView from "../components/tasks/TaskListView.vue";
import CurrentSessionView from "../components/session/CurrentSessionView.vue";
import NewSessionSetup from "@/components/session/NewSessionSetup.vue";
import SpaceListView from "@/components/spaces/SpaceListView.vue";
import NewSpaceSetup from "@/components/spaces/NewSpaceSetup.vue";

import { store as currentSpaceStore } from "@/stores/current_space";

export default {
  components: {
    TaskListView,
    CurrentSessionView,
    NewSessionSetup,
    SpaceListView,
    NewSpaceSetup,
  },

  data() {
    return {
      currentSpaceStore,
    };
  },

  computed: {
    isInSession(): boolean {
      return currentSpaceStore.inSession;
    },
  },

  async mounted() {
    await currentSpaceStore.init();
  },

  methods: {
    beginSession() {
      currentSpaceStore.inSession = true;
    },

    endSession() {
      currentSpaceStore.inSession = false;
    },
  },
};
</script>

<template>
  <div class="vh-100 vw-100 p-4 hstack">
    <div class="h-100 w-50 me-3">
      <TaskListView :in-session="isInSession" />
    </div>
    <div class="h-100 w-50">
      <CurrentSessionView v-if="isInSession" @done="endSession" />
      <div v-else class="w-100 h-100 d-flex">
        <div class="w-100 h-100 d-flex flex-column align-items-stretch">
          <div class="mx-auto w-100 flex-shrink-0">
            <NewSessionSetup @done="beginSession" />
          </div>
          <div
            class="mx-auto w-100 mb-3 mt-3 flex-shrink-1 flex-fill"
            style="min-height: 0"
          >
            <SpaceListView />
          </div>
          <div class="mx-auto w-100 flex-shrink-0">
            <NewSpaceSetup />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
