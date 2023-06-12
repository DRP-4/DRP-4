import { describe, it, expect } from "vitest";

import { mount } from "@vue/test-utils";
import TaskListItem from "../tasks/TaskListItem.vue";
import type { Task } from "@/api/tasks";
import { Duration } from "@/api/duration";

describe("HelloWorld", () => {
  it("renders properly", () => {
    const task: Task = {
      name: "Do your work",
      id: 1,
      duration: new Duration(10),
      description: "<p>Sample description</p>",
      complete: false,
    };

    const wrapper = mount(TaskListItem, { props: { task } });
    expect(wrapper.text()).toContain("Sample description");
  });

  it("Knows about math", () => {
    let x = 2;

    x += 2;
    x = 4;

    expect(x).toBe(4);
  });
});
