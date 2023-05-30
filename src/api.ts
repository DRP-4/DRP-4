const API_BASE = import.meta.env.DEV
  ? "http://127.0.0.1:5000"
  : "https://drp-api.perial.co.uk";

export interface Task {
  name: string;
}

export async function getTasks(): Promise<Task[]> {
  const response = await fetch(`${API_BASE}/tasks`);
  const tasks = await response.json();
  return tasks;
}
