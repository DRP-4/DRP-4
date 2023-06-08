import { describe, it, expect } from "vitest";

import { mount } from "@vue/test-utils";
import TaskItem from "../TaskItem.vue";
import type { Task } from "@/api/tasks";

describe("HelloWorld", () => {
  it("renders properly", () => {
    const task: Task = {
      name: "Do your work",
      id: 1,
      duration: 10,
      description: "<p>Sus</p>",
      complete: false,
    };

    const wrapper = mount(TaskItem, { props: { task } });
    expect(wrapper.text()).toContain("Do your work");
  });

  it("Knows about math", () => {
    let x = 2;

    x += 2;
    x = 4;

    expect(x).toBe(4);
  });
});
