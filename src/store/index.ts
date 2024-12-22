// store/index.ts
import { createStore } from 'vuex';
import bookModule from './modules/book';
import userModule from './modules/user';
import orderModule from './modules/order';
import recordModule from './modules/shortage';
import procureModule from './modules/procure';
import supplierModule from './modules/supplier';

export default createStore({
  modules: {
    book: bookModule,
    user: userModule,
    order: orderModule,
    record: recordModule,
    procure: procureModule,
    supplier: supplierModule,
  },
});
