<script lang="ts">
import Satisifed from "@/components/icons/SatisfiedFace.vue";
import Neutral from "@/components/icons/NeutralFace.vue";
import Dissatisfied from "@/components/icons/DissatisfiedFace.vue";

export default {
  components: {
    Satisifed,
    Neutral,
    Dissatisfied,
  },
  props: {
    name: {
      type: String,
      required: true,
    },
  },
  emits: ["satisfied", "neutral", "dissatisfied"],
};
</script>

<template>
  <div class="centered">
    <div class="form-horizontal border p-3 rounded">
      <div class="centered">
        <h2>How was session {{ name }}?</h2>
      </div>

      <div class="centered">
        <div class="emotions">
          <div class="face" @click="$emit('satisfied')">
            <Satisifed />
          </div>
          <div class="face" @click="$emit('neutral')">
            <Neutral />
          </div>
          <div class="face" @click="$emit('dissatisfied')">
            <Dissatisfied />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.centered {
  display: flex;
  align-items: center;
  justify-content: center;
}

.emotions {
  display: flex;
  gap: 2em;
  margin: 1em;
}

.face {
  transition: transform 0.2s;
}

.face:hover {
  transform: scale(1.2);
}
</style>
