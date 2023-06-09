import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("../views/HomeView.vue"),
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/session",
      component: () => import("../views/SessionTimerView.vue"),
    },
    {
      path: "/demos/session_done",
      component: () => import("../views/SessionDoneDemo.vue"),
    },
    {
      path: "/demos/task_view",
      component: () => import("../views/TaskViewDemo.vue"),
    },
    {
      path: "/demos/new_home",
      component: () => import("../views/NewHomeDemo.vue"),
    },
  ],
});

export default router;
