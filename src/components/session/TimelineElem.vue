<script lang="ts">
export default {
  props: {
    startingTime: {
      type: Date,
      required: true,
    },
    height: {
      type: String,
      required: true,
    },
    isWork: Boolean,
    inProgress: Boolean,
    ahead: Boolean,
  },
};
</script>

<template>
  <div class="w-100 d-flex flex-column" :style="{ height }">
    <div>
      <small>{{ startingTime.toTimeString().slice(0, 5) }}</small>
    </div>
    <div class="flex-grow-1 hstack">
      <div class="h-100" style="width: 4.375ex">
        <div
          :class="{
            line: true,
            'h-100': true,
            break: !isWork,
            work: isWork,
            'in-progress': inProgress,
            ahead: ahead,
          }"
        ></div>
      </div>
      <div class="me-auto w-100 h-100">
        <div class="card w-100 h-100">
          <div class="card-body p-2 w-100 h-100 overflow-scroll">
            <slot />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style stacked>
.line {
  width: 15px;
  margin-left: auto;
  margin-right: auto;
  border: rounded;
  border-radius: 7px;
}

.work {
  background-color: #465298;
}

.break {
  background-color: #bc6d60;
}

.in-progress {
  animation: barberpole 10s linear infinite;
}

.work.in-progress {
  background: repeating-linear-gradient(
    45deg,
    #606dbc,
    #606dbc 10px,
    #465298 10px,
    #465298 20px
  );
}

.break.in-progress {
  background: repeating-linear-gradient(
    45deg,
    #bc6d60,
    #bc6d60 10px,
    #985246 10px,
    #985246 20px
  );
}

.ahead {
  opacity: 0.5;
}
</style>
