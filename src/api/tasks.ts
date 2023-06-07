import { post, get } from "@/api";

export interface Task {
  name: string;
  id: number;
  duration: number;
}

export interface CreateTask {
  name: string;
  // Client doens't get to specify ID, it's auto-incremented
  // by postgres
}

// return all tasks for users current session
export async function tasks(): Promise<Task[]> {
  return get("tasks");
}

// update whether a task has been completed
export async function updateTask(id: number, complete: boolean) {
  return post("update-task", { id, complete });
}
