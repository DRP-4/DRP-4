import { get, post } from "@/api"

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
    return get("tasks");
}

export async function addTask(task: CreateTask) {
    return post("tasks", task);
}
