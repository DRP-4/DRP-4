import { post, get, del, put } from "@/api";
import { Duration } from "./duration";

export type TaskID = number;

export class Task {
  public id: TaskID;
  public name: string;
  public duration?: Duration;
  public description?: string;
  public complete: boolean;

  public constructor(
    id: number,
    name: string,
    cfg: { duration?: Duration; description?: string; complete?: boolean }
  ) {
    this.id = id;
    this.name = name;
    this.description = cfg?.description;
    this.duration = cfg?.duration;
    this.complete = cfg?.complete === undefined ? false : cfg?.complete;
  }
}

export interface TaskUpdate {
  id: TaskID;
  duration?: Duration;
  name?: string;
  description?: string;
  complete?: boolean;
}

// Create a new task given name, duration and description
export async function createTask(
  cfg: {name: string, description?: string}
): Promise<TaskID> {
  const resp = await ((await post("task/create", cfg)).json());
  return resp.id;
}

// return all tasks for users current session
export async function tasks(): Promise<Map<TaskID, Task>> {
  const apiTasks: {
    id: number;
    name: string;
    description: string | null;
    duration: number | null;
    completed: boolean;
  }[] = await get("task/get-all");
  const result = new Map<TaskID, Task>();

  apiTasks.forEach((apiTask) => {
    result.set(
      apiTask.id,
      new Task(apiTask.id, apiTask.name, {
        description:
          apiTask.description === null ? undefined : apiTask.description,
        duration:
          apiTask.duration === null
            ? undefined
            : new Duration(apiTask.duration),
        complete: apiTask.completed,
      })
    );
  });

  return result;
}

// update whether a task has been completed
export async function updateTask(update: TaskUpdate) {
  return put("task/update", {
    id: update.id,
    name: update.name,
    duration: update.duration?.minutes,
    description: update.description,
    complete: update.complete,
  });
}

// delete a task given its id
export async function deleteTask(id: TaskID) {
  return del("task/delete", { id });
}
