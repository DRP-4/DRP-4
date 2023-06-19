import "./assets/main.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import { store as timeJumpStore } from "./stores/time_jump";

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount("#app");

(async () => {
  await timeJumpStore.fetchFromDB();
})();
