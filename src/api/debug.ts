import { post } from "@/api";
import { store } from "@/stores/time_jump";

export async function jumpSeconds(seconds: number) {
  store.jump(seconds);
  return await post("debug/jump-seconds", { seconds: store.deltaInSeconds });
}

export async function resetJumpCounter() {
  store.jump(0);
  return await post("debug/jump-seconds", { seconds: 0 });
}
