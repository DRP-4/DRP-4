import { describe, it, expect } from "vitest";

import { mount } from "@vue/test-utils";
import Task from "../Task.vue";

describe("HelloWorld", () => {
  it("renders properly", () => {

    const task = {
      name: "Do your work"
    };

    const wrapper = mount(Task, { props: { task } });
    expect(wrapper.text()).toContain("Do your work");
  });
});
