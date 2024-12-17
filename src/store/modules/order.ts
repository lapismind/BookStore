// store/modules/order.ts
import { GetterTree, MutationTree, ActionTree } from 'vuex';
import { Order, ProcurementOrder } from '@/store/modules/types';

interface OrderState {
  orders: Order[];
  procurementOrders: ProcurementOrder[];
}

const state: OrderState = {
  orders: [],
  procurementOrders: [],
};

const getters: GetterTree<OrderState, any> = {
  orders: (state: OrderState) => state.orders,
  getOrderById: (state) => (orderId: number) => {
    return state.orders.find(order => order.order_id === orderId);
  },
  procurementOrders: (state: OrderState) => state.procurementOrders,
  getProcurementOrderByBookId: (state) => (bookId: number) => {
    return state.procurementOrders.find(order => order.book_id === bookId);
  },
};

const actions: ActionTree<OrderState, any> = {
  addOrder({ commit }, order: Order) {
    commit('ADD_ORDER', order);
  },
  updateOrder({ commit }, updatedOrder: Order) {
    commit('UPDATE_ORDER', updatedOrder);
  },
  deleteOrder({ commit }, orderId: number) {
    commit('DELETE_ORDER', orderId);
  },
  addProcurementOrder({ commit }, order: ProcurementOrder) {
    commit('ADD_PROCUREMENT_ORDER', order);
  },
  updateProcurementOrder({ commit }, updatedOrder: ProcurementOrder) {
    commit('UPDATE_PROCUREMENT_ORDER', updatedOrder);
  },
  deleteProcurementOrder({ commit }, procurementOrderId: number) {
    commit('DELETE_PROCUREMENT_ORDER', procurementOrderId);
  },
  async fetchProcurementOrders({ commit }) {
    try {
      const initialOrders: ProcurementOrder[] = [
        {
          procurement_order_id: 1,
          book_id: 101,
          quantity: 10,
          status: 'pending',
        },
      ];
      commit('SET_PROCUREMENT_ORDERS', initialOrders);
    } catch (error) {
      console.error('Failed to fetch procurement orders:', error);
      throw error;
    }
  },
};

const mutations: MutationTree<OrderState> = {
  ADD_ORDER(state, order: Order) {
    state.orders.push(order);
  },
  UPDATE_ORDER(state, updatedOrder: Order) {
    const index = state.orders.findIndex(order => order.order_id === updatedOrder.order_id);
    if (index !== -1) {
      state.orders.splice(index, 1, updatedOrder);
    }
  },
  DELETE_ORDER(state, orderId: number) {
    state.orders = state.orders.filter(order => order.order_id !== orderId);
  },
  ADD_PROCUREMENT_ORDER(state, order: ProcurementOrder) {
    state.procurementOrders.push(order);
  },
  UPDATE_PROCUREMENT_ORDER(state, updatedOrder: ProcurementOrder) {
    const index = state.procurementOrders.findIndex(order => order.procurement_order_id === updatedOrder.procurement_order_id);
    if (index !== -1) {
      state.procurementOrders.splice(index, 1, updatedOrder);
    }
  },
  DELETE_PROCUREMENT_ORDER(state, procurementOrderId: number) {
    state.procurementOrders = state.procurementOrders.filter(order => order.procurement_order_id !== procurementOrderId);
  },
  SET_PROCUREMENT_ORDERS(state, orders: ProcurementOrder[]) {
    state.procurementOrders = orders;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};