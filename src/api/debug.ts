import { post } from "@/api";

export async function jumpSeconds(seconds: number) {
  return await post("/debug/jump-seconds", { seconds });
}
