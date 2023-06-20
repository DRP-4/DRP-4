<script lang="ts">
import { isInSession } from "@/api/session";
import TaskListView from "../components/tasks/TaskListView.vue";
import CurrentSessionView from "../components/session/CurrentSessionView.vue";
import NewSessionSetup from "@/components/session/NewSessionSetup.vue";

export default {
  components: {
    TaskListView,
    CurrentSessionView,
    NewSessionSetup,
  },
  data() {
    return {
      fakeKey: 0,
      inSession: false,
    };
  },

  async created() {
    this.inSession = await isInSession();
  },

  methods: {
    beginSession() {
      this.fakeKey += 2;
      this.inSession = true;
    },

    endSession() {
      this.fakeKey += 2;
      this.inSession = false;
    },
  },
};
</script>

<template>
  <div class="vh-100 vw-100 p-4 hstack">
    <div class="h-100 w-50 me-3">
      <TaskListView :in-session="inSession" />
    </div>
    <div class="h-100 w-50 ms-3">
      <CurrentSessionView v-if="inSession" @done="endSession" />
      <div v-else class="card w-100 h-100 d-flex">
        <div class="m-auto">
          <NewSessionSetup @done="beginSession" />
        </div>
      </div>
    </div>
  </div>
</template>
