// store/modules/record.ts
import { GetterTree, MutationTree, ActionTree } from 'vuex';
import { BookShortage } from '@/store/modules/types';

interface RecordState {
  shortageRecords: BookShortage[];
}

const state: RecordState = {
  shortageRecords: [],
};

const getters: GetterTree<RecordState, any> = {
  shortageRecords: (state: RecordState) => state.shortageRecords,
  getShortageRecordById: (state) => (shortageId: number) => {
    return state.shortageRecords.find(record => record.shortage_id === shortageId);
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
};

const actions: ActionTree<RecordState, any> = {
  fetchShortageRecords({ commit }) {
    try {
      // 假设这里是一个API调用，我们使用模拟数据
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
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};