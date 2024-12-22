import { ActionContext,GetterTree, MutationTree, ActionTree, Module } from 'vuex';
import axios from 'axios';
import { ProcurementOrder } from '@/store/modules/types';

class ProcurementState {
  procurementOrders: ProcurementOrder[] = [];
}

class ProcurementGetters implements GetterTree<ProcurementState, any> {
  [key: string]: any;

  procurementOrders = (state: ProcurementState) => state.procurementOrders;
  getProcurementOrderById = (state: ProcurementState) => (procurementOrderId: number) => {
    return state.procurementOrders.find(order => order.procurement_order_id === procurementOrderId);
  };
}

class ProcurementMutations implements MutationTree<ProcurementState> {
  [key: string]: any;

  ADD_PROCUREMENT_ORDER(state: ProcurementState, order: ProcurementOrder) {
    state.procurementOrders.push(order);
  }
  SET_PROCUREMENT_ORDERS(state: ProcurementState, orders: ProcurementOrder[]) {
    state.procurementOrders = orders;
  }
  UPDATE_PROCUREMENT_ORDER(state: ProcurementState, updatedOrder: ProcurementOrder) {
    const index = state.procurementOrders.findIndex(order => order.procurement_order_id === updatedOrder.procurement_order_id);
    if (index !== -1) {
      state.procurementOrders.splice(index, 1, updatedOrder);
    }
  }
}

class ProcurementActions implements ActionTree<ProcurementState, any> {
  [key: string]: any;

  async addProcurementOrder({ commit }: ActionContext<ProcurementState, any>, order: ProcurementOrder) {
    try {
      await axios.post('/procure/add', order);
      commit('ADD_PROCUREMENT_ORDER', order);
    } catch (error) {
      console.error('Failed to add procurement order:', error);
      throw error;
    }
  }

  async fetchProcurementOrders({ commit }: ActionContext<ProcurementState, any>) {
    try {
      const response = await axios.get('/procure/get');
      commit('SET_PROCUREMENT_ORDERS', response.data);
    } catch (error) {
      console.error('Failed to fetch procurement orders:', error);
      throw error;
    }
  }

  async updateProcurementOrder({ commit }: ActionContext<ProcurementState, any>, updatedOrder: ProcurementOrder) {
    try {
      await axios.put(`/procure/change/${updatedOrder.procurement_order_id}`, updatedOrder);
      commit('UPDATE_PROCUREMENT_ORDER', updatedOrder);
    } catch (error) {
      console.error('Failed to update procurement order:', error);
      throw error;
    }
  }
}

const state = new ProcurementState();
const getters = new ProcurementGetters();
const mutations = new ProcurementMutations();
const actions = new ProcurementActions();

const procureModule: Module<ProcurementState, any> = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};

export default procureModule;