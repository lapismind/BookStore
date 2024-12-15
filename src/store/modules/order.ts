// store/modules/order.ts
import { GetterTree, MutationTree, ActionTree } from 'vuex';
import { Order } from '@/store/modules/types'; // 确保导入 Order 接口

interface OrderState {
  orders: Order[];
}

const state: OrderState = {
  orders: [], // 初始化为空数组
};

const getters: GetterTree<OrderState, any> = {
  orders: (state: OrderState) => state.orders,
  getOrderById: (state) => (orderId: number) => {
    return state.orders.find(order => order.order_id === orderId);
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
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
