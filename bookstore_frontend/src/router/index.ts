import { createRouter, createWebHistory } from "vue-router";
import BookBrowser from "@/pages/BookBrowser.vue"; // 确保路径与实际项目结构一致

const routes = [
  {
    path: "/book-browser",
    name: "BookBrowser",
    component: BookBrowser,
  },
];

const router = createRouter({
  history: createWebHistory(), // 使用 HTML5 History 模式
  routes,
});

export default router;
