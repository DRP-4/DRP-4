import { reactive } from "vue";
import { setJumpCounter, getJumpCounter } from "@/api/debug";
import { socket } from "@/api";

export const store = reactive({
  deltaInSeconds: 0,

  async fetchFromDB() {
    this.deltaInSeconds = await getJumpCounter();
  },

  async jump(by: number) {
    this.deltaInSeconds += by;
    await setJumpCounter(this.deltaInSeconds);
  },

  async reset() {
    this.deltaInSeconds = 0;
    await setJumpCounter(0);
  },

  dateWithDebugOffset(): Date {
    const thisInstant = new Date();
    const thisInstantUnix = thisInstant.getTime();
    const newInstantUnix = thisInstantUnix + this.deltaInSeconds * 1000;
    const newInstant = new Date(newInstantUnix);
    return newInstant;
  },
});

socket.on("jump-seconds", (data) => {
  const newDelta = data.seconds;
  // If statement is needed to not trigger unnecessary reactive updates
  if (store.deltaInSeconds != newDelta) {
    store.deltaInSeconds = newDelta;
  }
});
