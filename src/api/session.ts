import { post, get } from "@/api";
import { Task, type APITask } from "@/api/tasks";

export interface Slot {
  start: Date;
  end: Date;
  is_work: Boolean;
  completed_tasks: Task[];
}

export interface Session {
  start: Date;
  end: Date;
  slots: Slot[];
}

// checks if there is a currently active session
export async function isInSession(): Promise<boolean> {
  return (await get("session/active")).active;
}

// make a new session and slots in the database, given a duration
// also deletes all completed tasks
export async function newSession(duration: number) {
  return post("session/new", { duration });
}

// stops the current session
export async function endSession() {
  return post("session/end", {});
}

// get the current session for this user
export async function getSession(): Promise<Session> {
  const apiSession: {
    start_unix: number;
    end_unix: number;
    slots: {
      start_unix: number;
      end_unix: number;
      is_work: boolean;
      completed_tasks: APITask[];
    }[];
  } = await get("session/current");

  return {
    start: new Date(apiSession.start_unix * 1000),
    end: new Date(apiSession.end_unix * 1000),
    slots: apiSession.slots.map((apiSlot) => {
      return {
        start: new Date(apiSlot.start_unix * 1000),
        end: new Date(apiSlot.end_unix * 1000),
        is_work: apiSlot.is_work,
        completed_tasks: apiSlot.completed_tasks.map((apiTask) =>
          Task.parseFromAPI(apiTask)
        ),
      };
    }),
  };
}
