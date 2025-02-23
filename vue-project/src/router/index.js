import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ScoreView from "../views/ScoreView.vue";

// Enables web routing
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/score",
      name: "score",
      component: ScoreView,
    },
  ],
});

export default router;
