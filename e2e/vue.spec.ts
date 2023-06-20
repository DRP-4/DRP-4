import { test } from "@playwright/test";

test("creates a new task", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Add new task" }).click();
  await page.getByPlaceholder("Task name (required)").click();
  await page.getByPlaceholder("Task name (required)").fill("Add new task");
  await page.getByLabel("Add description (optional)").check();
  await page.locator(".ql-editor").click();
  await page.locator(".ql-editor").fill("Add description");
  await page
    .getByRole("dialog", { name: "Add new task" })
    .getByRole("button", { name: "Add new task" })
    .click();
});

test("creates a new session", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Create session" }).click();
});

test("creates a new space", async ({ page }) => {
  await page.goto("/");

  await page.getByPlaceholder("Display name").click();
  await page.getByPlaceholder("Display name").fill("");
  await page.locator(".input-group").click();
  await page.getByPlaceholder("Display name").fill("DRP-04");
  await page.getByRole("button", { name: "Create", exact: true }).click();
});
