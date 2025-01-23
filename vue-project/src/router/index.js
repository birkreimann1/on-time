import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ListView from "../views/ListView.vue";
import ScoreView from "../views/ScoreView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/list",
      name: "list",
      component: ListView,
    },
    {
      path: "/score",
      name: "score",
      component: ScoreView,
    },
  ],
});

export default router;
