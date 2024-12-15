// store/index.ts
import { createStore } from 'vuex';
import bookModule from './modules/book';
import userModule from './modules/user';
import orderModule from './modules/order';

export default createStore({
  modules: {
    book: bookModule,
    user: userModule,
    order: orderModule,
  },
});
