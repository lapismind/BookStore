import { ActionContext, GetterTree, MutationTree, ActionTree, Module } from 'vuex';
import apiClient from '@/api';
import { ProcurementOrder } from '@/store/modules/types';

interface ProcurementState {
  procurementOrders: ProcurementOrder[];
}

const state: ProcurementState = {
  procurementOrders: [],
};

const getters: GetterTree<ProcurementState, any> = {
  procurementOrders: (state: ProcurementState) => state.procurementOrders,
  getProcurementOrderById: (state) => (procurementOrderId: number) => {
    return state.procurementOrders.find(order => order.procurement_order_id === procurementOrderId);
  },
};

const mutations: MutationTree<ProcurementState> = {
  ADD_PROCUREMENT_ORDER(state: ProcurementState, order: ProcurementOrder) {
    state.procurementOrders.push(order);
  },
  SET_PROCUREMENT_ORDERS(state: ProcurementState, orders: ProcurementOrder[]) {
    state.procurementOrders = orders;
  },
  UPDATE_PROCUREMENT_ORDER(state: ProcurementState, updatedOrder: ProcurementOrder) {
    const index = state.procurementOrders.findIndex(order => order.procurement_order_id === updatedOrder.procurement_order_id);
    if (index !== -1) {
      state.procurementOrders.splice(index, 1, updatedOrder);
    }
  },
};

const actions: ActionTree<ProcurementState, any> = {
  async addProcurementOrder({ commit }: ActionContext<ProcurementState, any>, order: ProcurementOrder) {
    try {
      const response = await apiClient.post('/procure/create', order);
      commit('ADD_PROCUREMENT_ORDER', response.data);
    } catch (error) {
      console.error('Failed to add procurement order:', error);
      throw error;
    }
  },
  async fetchProcurementOrders({ commit }: ActionContext<ProcurementState, any>) {
    try {
      const response = await apiClient.get('/procure/list');
      commit('SET_PROCUREMENT_ORDERS', response.data.procurements);
    } catch (error) {
      console.error('Failed to fetch procurement orders:', error);
      throw error;
    }
  },
  async completeProcurementOrder({ commit }: ActionContext<ProcurementState, any>, procurementOrderId: number) {
    try {
      const response = await apiClient.post('/procure/complete', { procurement_order_id: procurementOrderId });
      commit('UPDATE_PROCUREMENT_ORDER', response.data);
    } catch (error) {
      console.error('Failed to complete procurement order:', error);
      throw error;
    }
  }
};

const procureModule: Module<ProcurementState, any> = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};

export default procureModule;