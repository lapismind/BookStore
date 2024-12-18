import { createRouter, createWebHistory } from "vue-router";

import Home from "@/pages/Home.vue";
import BookBrowser from "@/pages/BookBrowser.vue";
import BookList from "@/pages/BookList.vue";
import BookManage from "@/pages/BookManage.vue";
import UserManage from "@/pages/UserManage.vue";
import OrderManage from "@/pages/OrderManage.vue";
import SupplierManage from "@/pages/SupplierManage.vue";
import Search from "@/pages/Search.vue";

const routes = [
  {
    path: "/",
    redirect: "/home",
  },
  {
    path: "/book-list",
    name: "BookList",
    component: BookList,
  },
  {
    path: "/book-browser",
    name: "BookBrowser",
    component: BookBrowser,
  },
  {
    path: "/book-manage",
    name: "BookManage",
    component: BookManage,
  },
  {
    path: "/user-manage",
    name: "UserManage",
    component: UserManage,
  },
  {
    path: "/order-manage",
    name: "OrderManage",
    component: OrderManage,
  },
  {
    path: "/supplier-manage",
    name: "SupplierManage",
    component: SupplierManage,
  },
  {
    path:"/search",
    name:"Search",
    component: Search,
  },
  {
    path: "/home",
    name: "Home",
    component: Home,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
