// store/modules/order.ts
import { GetterTree, MutationTree, ActionTree } from 'vuex';
import { Order } from '@/store/modules/types';
import axios from 'axios';

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
      await axios.post('/order/add', order);
      commit('ADD_ORDER', order);
    } catch (error) {
      console.error('Failed to add order:', error);
      throw error;
    }
  },
  async fetchOrders({ commit }) {
    try {
      const response = await axios.get('/order/get');
      commit('SET_ORDERS', response.data);
    } catch (error : any) {
      if (error.response && error.response.status === 404) {
        commit('SET_ORDERS', []); // Set orders to an empty array if 404
      } else {
        console.error('Failed to fetch orders:', error);
        throw error;
      }
    }
  },
  async updateOrder({ commit }, updatedOrder: Order) {
    try {
      await axios.put(`/order/change/${updatedOrder.order_id}`, updatedOrder);
      commit('UPDATE_ORDER', updatedOrder);
    } catch (error) {
      console.error('Failed to update order:', error);
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