import { post, get } from "@/api";
import type { Task } from "@/api/tasks";

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

// make a new session and slots in the database, given a duration
// also deletes all completed tasks
export async function newSession(duration: number) {
  return post("session/new", { duration });
}

// get the current session for this user
export async function getSession(): Promise<Session> {
  return get("session/current");
}
