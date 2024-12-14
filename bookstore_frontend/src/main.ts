import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // 引入刚创建的路由实例

const app = createApp(App);
app.use(router); // 使用 Vue Router
app.mount("#app");
