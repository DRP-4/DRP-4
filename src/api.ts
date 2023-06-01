const API_BASE = import.meta.env.DEV
  ? "http://127.0.0.1:5000"
  : "https://drp-04.herokuapp.com/";

export interface Task {
  name: string;
  id: number;
}

export async function getTasks(): Promise<Task[]> {
  const response = await fetch(`${API_BASE}/api/tasks`);
  const tasks = await response.json();
  return tasks;
}
