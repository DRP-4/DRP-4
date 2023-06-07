import { post } from "@/api";
import { Task } from "@/tasks";

export interface Slot {
  start: Date;
  end: Date;
  is_work: Boolean;
  completed_tasks: Task[];
}

export interface Session {
  start: Date;
  end: Date;
  current_slot: Slot;
  past_slots: Slot[];
}

// make a new session and slots in the database, given some tasks and a duration
export async function newSession(tasks: string[], duration: number) {
  return post("new-session", { tasks, duration });
}

// get the current session for this user
export async function getSession(): Session {
  return get("current-session");
}
