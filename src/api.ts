const API_BASE = import.meta.env.DEV
  ? "http://127.0.0.1:5000"
  : "https://drp-04.herokuapp.com/";

export interface Task {
  name: string;
  id: number;
}

export interface CreateTask {
  name: string;
  // Client doens't get to specify ID, it's auto-incremented
  // by postgres
}

export async function getTasks(): Promise<Task[]> {
  const response = await fetch(`${API_BASE}/api/tasks`);
  const tasks = await response.json();
  return tasks;
}

async function post(route: string, value: any): Promise<Response> {
  const body = JSON.stringify(value);
  const response = await fetch(`${API_BASE}/api/${route}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body,
  });
  return response;
}

export async function addTask(task: CreateTask) {
  return post("tasks", task);
}
