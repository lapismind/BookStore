import { GetterTree, MutationTree, ActionTree } from 'vuex';
import { Order } from '@/store/modules/types';
import apiClient from '@/api';

interface OrderState {
  orders: Order[];
}

const state: OrderState = {
  orders: [],
};

const getters: GetterTree<OrderState, any> = {
  orders: (state: OrderState) => state.orders,
  getOrderById: (state) => (orderId: number) => {
    return state.orders.find(order => order.order_id === orderId);
  },
  getOrdersByReaderId: (state) => (readerId: number) => {
    return state.orders.filter(order => order.reader_id === readerId);
  },
};

const actions: ActionTree<OrderState, any> = {
  async addOrder({ commit }, order: Order) {
    try {
      const response = await apiClient.post('/order/add', order);
      commit('ADD_ORDER', response.data);
    } catch (error) {
      console.error('Failed to add order:', error);
      throw error;
    }
  },
  async fetchOrders({ commit }) {
    try {
      const response = await apiClient.get('/order/list');
      commit('SET_ORDERS', response.data.orders);
    } catch (error) {
      console.error('Failed to fetch orders:', error);
      throw error;
    }
  },
  async shipOrder({ commit }, orderId: number) {
    try {
      const response = await apiClient.post('/order/ship', { order_id: orderId });
      commit('UPDATE_ORDER', response.data);
    } catch (error) {
      console.error('Failed to ship order:', error);
      throw error;
    }
  },
  async receiveOrder({ commit }, orderId: number) {
    try {
      const response = await apiClient.post('/order/receive', { order_id: orderId });
      commit('UPDATE_ORDER', response.data);
    } catch (error) {
      console.error('Failed to receive order:', error);
      throw error;
    }
  },
};

const mutations: MutationTree<OrderState> = {
  ADD_ORDER(state, order: Order) {
    state.orders.push(order);
  },
  SET_ORDERS(state, orders: Order[]) {
    state.orders = orders;
  },
  UPDATE_ORDER(state, updatedOrder: Order) {
    const index = state.orders.findIndex(order => order.order_id === updatedOrder.order_id);
    if (index !== -1) {
      state.orders.splice(index, 1, updatedOrder);
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};