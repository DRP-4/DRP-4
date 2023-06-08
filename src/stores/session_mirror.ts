import { reactive } from "vue";
import type { Task } from "@/api/tasks";

export default reactive({
  duration_mins: 0,
  tasks_todo: <Task[]>[],
});
