import { GetterTree, MutationTree, ActionTree, Module, ActionContext } from 'vuex';
import apiClient from '@/api';
import { Supplier } from '@/store/modules/types';

interface SupplierState {
  suppliers: Supplier[];
}

const state: SupplierState = {
  suppliers: [],
};

const getters: GetterTree<SupplierState, any> = {
  suppliers: (state: SupplierState) => state.suppliers,
};

const mutations: MutationTree<SupplierState> = {
  ADD_SUPPLIER(state: SupplierState, supplier: Supplier) {
    state.suppliers.push(supplier);
  },
  SET_SUPPLIERS(state: SupplierState, suppliers: Supplier[]) {
    state.suppliers = suppliers;
  },
};

const actions: ActionTree<SupplierState, any> = {
  async addSupplier({ commit }: ActionContext<SupplierState, any>, supplier: Supplier) {
    try {
      const response = await apiClient.post('/supplier/add', supplier);
      commit('ADD_SUPPLIER', response.data.supplier);
    } catch (error) {
      console.error('Failed to add supplier:', error);
      throw error;
    }
  },
  async fetchSuppliers({ commit }: ActionContext<SupplierState, any>) {
    try {
      const response = await apiClient.get('/supplier/query');
      commit('SET_SUPPLIERS', response.data.suppliers);
    } catch (error) {
      console.error('Failed to fetch suppliers:', error);
      throw error;
    }
  },
};

const supplierModule: Module<SupplierState, any> = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};

export default supplierModule;