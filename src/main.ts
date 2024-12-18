import { createApp } from "vue";
import App from "./App.vue";
import store from './store';
import router from "./router";
import "./styles/global.css";

if (process.env.NODE_ENV === 'production') {
  process.env.__VUE_PROD_HYDRATION_MISMATCH_DETAILS__ = process.env.VUE_APP__VUE_PROD_HYDRATION_MISMATCH_DETAILS || 'false';
}

const app = createApp(App);

app.use(router);
app.use(store);

app.mount("#app");
