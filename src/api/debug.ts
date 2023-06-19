import { get, post } from "@/api";

export async function getJumpCounter(): Promise<number> {
  return (await get("debug/jump-seconds")).seconds;
}

export async function setJumpCounter(seconds: number) {
  return await post("debug/jump-seconds", { seconds: seconds });
}
