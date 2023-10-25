import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: "/trucks",
    name: "trucks",
    component: () =>
      import(/* webpackChunkName: "trucks" */ "../views/TrucksView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/LoginView.vue"),
    meta: { requiresAuth: false },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  if (!requiresAuth) {
    next();
    return;
  }

  try {
    await store.dispatch("checkAuthentication");
    const isAuthenticated = store.state.isAuthenticated;

    if (!isAuthenticated) {
      next({ name: "login" });
    } else {
      next();
    }
  } catch (error) {
    console.error("Error during route guard execution:", error);
    next(false);
  }
});

export default router;
