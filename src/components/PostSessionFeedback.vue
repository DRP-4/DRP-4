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
  <div class="modal-dialog modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-body">
        <div class="form-horizontal p-3 rounded">
          <div class="centered">
            <h2>How was session {{ name }}?</h2>
          </div>

          <div class="centered">
            <div class="emotions">
              <button
                type="button"
                class="btn face close"
                data-bs-dismiss="modal"
                @click="$emit('satisfied')"
              >
                <Satisifed />
              </button>
              <button
                type="button"
                class="btn face close"
                data-bs-dismiss="modal"
                @click="$emit('neutral')"
              >
                <Neutral />
              </button>
              <button
                type="button"
                class="btn face close"
                data-bs-dismiss="modal"
                @click="$emit('dissatisfied')"
              >
                <Dissatisfied />
              </button>
            </div>
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
