import { createRouter, createWebHistory } from "vue-router";
import BookBrowser from "@/pages/BookBrowser.vue";
import BookManage from "@/pages/BookManage.vue";
import Home from "@/pages/Home.vue";

const routes = [
  {
    path: "/book-browser",
    name: "BookBrowser",
    component: BookBrowser,
  },
  {
    path: "/",
    redirect: "/home",
  },
  {
    path: "/book-manage",
    name: "BookManage",
    component: BookManage,
  },
  {
    path: "/home",
    name: "Home",
    component: Home,
  },
];

const router = createRouter({
  history: createWebHistory(), // 使用 HTML5 History 模式
  routes,
});

export default router;
