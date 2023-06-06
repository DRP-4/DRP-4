import { post } from "@/api";

export interface Task {
  name: string;
  id: number;
}

export interface CreateTask {
  name: string;
  // Client doens't get to specify ID, it's auto-incremented
  // by postgres
}

export async function newSession(tasks: string[], duration: number) {
  return post("new-session", { tasks, duration });
}
