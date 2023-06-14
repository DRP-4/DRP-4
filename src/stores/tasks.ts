import { reactive } from "vue";
import { type TaskID, Task, tasks, createTask, deleteTask } from "@/api/tasks";

export const store = reactive({
  tasks: new Map<TaskID, Task>(),

  async loadFromDB() {
    this.tasks = await tasks();
  },

  async add(newTask: { name: string; description?: string }) {
    const id = await createTask(newTask);
    this.tasks.set(
      id,
      new Task(id, newTask.name, { description: newTask.description })
    );
  },

  update(task: Task) {
    this.tasks.set(task.id, task);
  },

  async remove(id: TaskID) {
    this.tasks.delete(id);
    await deleteTask(id);
  },

  sortedTasksList(): Task[] {
    return [...this.tasks.values()].sort((l, r) => l.id - r.id);
  },
});
