<script lang="ts">
export default {
  props: {
    startingTime: {
      type: Date,
      required: true,
    },
    height: {
      type: Number,
      required: true,
    },
    isWork: Boolean,
    completeness: {
      type: Number,
      required: true,
    },
  },
};
</script>

<template>
  <div class="w-100 d-flex flex-column" :style="`height: ${height}em`">
    <div>
      <small>{{ startingTime.toTimeString().slice(0, 5) }}</small>
    </div>
    <div class="flex-grow-1 hstack">
      <div class="h-100" style="width: 4.375ex">
        <div
          :class="{
            'line-background': true,
            'h-100': true,
            break: !isWork,
            work: isWork,
            done: completeness >= 1.0,
          }"
        >
          <div
            v-if="completeness > 0.01 && completeness < 1.0"
            :class="{
              'line-progress': true,
              break: !isWork,
              work: isWork,
            }"
            :style="{
              height: `${completeness * 100}%`,
            }"
          ></div>
        </div>
      </div>
      <div class="me-auto w-100 h-100">
        <div class="card w-100 h-100">
          <div class="card-body p-2 w-100 h-100 overflow-visible">
            <slot />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style stacked>
.line-background {
  width: 15px;
  margin-left: auto;
  margin-right: auto;
  border: rounded;
  border-radius: 7px;
}

.line-progress {
  width: 100%;
  border: rounded;
  border-radius: 7px;
  opacity: initial;
  overflow: hidden;
}

.line-background.work {
  background-color: #4652988a;
}

.line-background.break {
  background-color: #bc6d608a;
}

.line-background.work.done {
  background-color: #465298;
}

.line-background.break.done {
  background-color: #bc6d60;
}

.line-progress.work {
  background: repeating-linear-gradient(
    45deg,
    #465298,
    #465298 10px,
    #323a6d 10px,
    #323a6d 20px
  );
  background-size: 28px 28px;
  animation: progress 0.8s linear infinite;
}

.line-progress.break {
  background: repeating-linear-gradient(
    45deg,
    #bc6d60,
    #bc6d60 10px,
    #b55546 10px,
    #b55546 20px
  );
  background-size: 28px 28px;
  animation: progress 0.8s linear infinite;
}

@keyframes progress {
  0% {
    background-position: 0 0;
  }

  100% {
    background-position: -28px 0px;
  }
}
</style>
