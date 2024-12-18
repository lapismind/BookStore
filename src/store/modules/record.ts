import { GetterTree, MutationTree, ActionTree } from 'vuex';
import { BookShortage, Inventory, Restock } from '@/store/modules/types';

interface RecordState {
  shortageRecords: BookShortage[];
  inventoryRecords: Inventory[];
  restockRecords: Restock[];
}

const state: RecordState = {
  shortageRecords: [],
  inventoryRecords: [],
  restockRecords: [],
};

const getters: GetterTree<RecordState, any> = {
  shortageRecords: (state: RecordState) => state.shortageRecords,
  getShortageRecordById: (state) => (shortageId: number) => {
    return state.shortageRecords.find(record => record.shortage_id === shortageId);
  },
  inventoryRecords: (state: RecordState) => state.inventoryRecords,
  getInventoryById: (state) => (inventoryId: number) => {
    return state.inventoryRecords.find(record => record.inventory_id === inventoryId);
  },
  restockRecords: (state: RecordState) => state.restockRecords,
  getRestockById: (state) => (restockId: number) => {
    return state.restockRecords.find(record => record.restock_id === restockId);
  },
};

const mutations: MutationTree<RecordState> = {
  SET_SHORTAGE_RECORDS(state, records: BookShortage[]) {
    state.shortageRecords = records;
  },
  ADD_SHORTAGE_RECORD(state, record: BookShortage) {
    state.shortageRecords.push(record);
  },
  UPDATE_SHORTAGE_RECORD(state, updatedRecord: BookShortage) {
    const index = state.shortageRecords.findIndex(record => record.shortage_id === updatedRecord.shortage_id);
    if (index !== -1) {
      state.shortageRecords.splice(index, 1, updatedRecord);
    }
  },
  DELETE_SHORTAGE_RECORD(state, shortageId: number) {
    state.shortageRecords = state.shortageRecords.filter(record => record.shortage_id !== shortageId);
  },
  SET_INVENTORY_RECORDS(state, records: Inventory[]) {
    state.inventoryRecords = records;
  },
  ADD_INVENTORY_RECORD(state, record: Inventory) {
    state.inventoryRecords.push(record);
  },
  UPDATE_INVENTORY_RECORD(state, updatedRecord: Inventory) {
    const index = state.inventoryRecords.findIndex(record => record.inventory_id === updatedRecord.inventory_id);
    if (index !== -1) {
      state.inventoryRecords.splice(index, 1, updatedRecord);
    }
  },
  DELETE_INVENTORY_RECORD(state, inventoryId: number) {
    state.inventoryRecords = state.inventoryRecords.filter(record => record.inventory_id !== inventoryId);
  },
  SET_RESTOCK_RECORDS(state, records: Restock[]) {
    state.restockRecords = records;
  },
  ADD_RESTOCK_RECORD(state, record: Restock) {
    state.restockRecords.push(record);
  },
  UPDATE_RESTOCK_RECORD(state, updatedRecord: Restock) {
    const index = state.restockRecords.findIndex(record => record.restock_id === updatedRecord.restock_id);
    if (index !== -1) {
      state.restockRecords.splice(index, 1, updatedRecord);
    }
  },
  DELETE_RESTOCK_RECORD(state, restockId: number) {
    state.restockRecords = state.restockRecords.filter(record => record.restock_id !== restockId);
  },
};

const actions: ActionTree<RecordState, any> = {
  fetchShortageRecords({ commit }) {
    try {
      const initialRecords: BookShortage[] = [
        {
          shortage_id: 1,
          book_id: 101,
          supplier: '供应商A',
          quantity: 5,
          record_date: new Date('2023-10-01'),
        }
      ];
      commit('SET_SHORTAGE_RECORDS', initialRecords);
    } catch (error) {
      console.error('Failed to fetch shortage records:', error);
      throw error;
    }
  },
  addShortageRecord({ commit }, record: BookShortage) {
    commit('ADD_SHORTAGE_RECORD', record);
  },
  updateShortageRecord({ commit }, updatedRecord: BookShortage) {
    commit('UPDATE_SHORTAGE_RECORD', updatedRecord);
  },
  deleteShortageRecord({ commit }, shortageId: number) {
    commit('DELETE_SHORTAGE_RECORD', shortageId);
  },
  fetchInventoryRecords({ commit }) {
    try {
      const initialRecords: Inventory[] = [
        {
          inventory_id: 1,
          book_id: 101,
          location: 'A1',
          status: 'available',
        }
      ];
      commit('SET_INVENTORY_RECORDS', initialRecords);
    } catch (error) {
      console.error('Failed to fetch inventory records:', error);
      throw error;
    }
  },
  addInventoryRecord({ commit }, record: Inventory) {
    commit('ADD_INVENTORY_RECORD', record);
  },
  updateInventoryRecord({ commit }, updatedRecord: Inventory) {
    commit('UPDATE_INVENTORY_RECORD', updatedRecord);
  },
  deleteInventoryRecord({ commit }, inventoryId: number) {
    commit('DELETE_INVENTORY_RECORD', inventoryId);
  },
  fetchRestockRecords({ commit }) {
    try {
      const initialRecords: Restock[] = [];
      commit('SET_RESTOCK_RECORDS', initialRecords);
    } catch (error) {
      console.error('Failed to fetch restock records:', error);
      throw error;
    }
  },
  addRestockRecord({ commit, state }, bookId: number) {
    const soldInventory = state.inventoryRecords.find(record => record.book_id === bookId && record.status === 'sold');
    if (soldInventory) {
      const newRestock: Restock = {
        restock_id: state.restockRecords.length + 1,
        book_id: bookId,
        inventory_id: soldInventory.inventory_id,
        restock_date: new Date(),
      };
      commit('ADD_RESTOCK_RECORD', newRestock);
      commit('UPDATE_INVENTORY_RECORD', { ...soldInventory, status: 'available' });
    } else {
      console.error('No sold inventory found for the given book ID');
    }
  },
  updateRestockRecord({ commit }, updatedRecord: Restock) {
    commit('UPDATE_RESTOCK_RECORD', updatedRecord);
  },
  deleteRestockRecord({ commit }, restockId: number) {
    commit('DELETE_RESTOCK_RECORD', restockId);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};