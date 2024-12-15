// store/index.js
import { createStore } from 'vuex';
import user from '@/store/modules/user';
import book from "@/store/modules/book";

export default createStore({
  modules: {
    user,
    book
  }
});