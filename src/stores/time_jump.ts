import { reactive } from "vue";

export const store = reactive({
  deltaInSeconds: 0,

  jump(by: number) {
    this.deltaInSeconds += by;
  },

  reset() {
    this.deltaInSeconds = 0;
  }
});
