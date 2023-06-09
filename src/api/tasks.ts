import { post, get, del, put } from "@/api";

export type TaskID = number;

export interface Task {
  id: TaskID;
  duration: number;
  name: string;
  description: string;
  complete: boolean;
}

export interface TaskUpdate {
  id: TaskID;
  duration?: number;
  name?: string;
  description?: string;
  complete?: boolean;
}

// Create a new task given name, duration and description
export async function createTask(name: string, duration: number, description: string) {
	return post("task/create", { name, duration, description });
}

// create a new task given only a name
export async function createTaskName(name: string) {
  return post("task/create", { name, "description": null, "duration": null });
}

// return all tasks for users current session
export async function tasks(): Promise<Task[]> {
  return get("task/get-all");
}

// update whether a task has been completed
export async function updateTask(update: TaskUpdate) {
  return put("task/update", update);
}

// delete a task given its id
export async function deleteTask(id: TaskID) {
  return del("task/delete", { id });
}
