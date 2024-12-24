import { GetterTree, MutationTree, ActionTree, Module, ActionContext } from 'vuex';
import apiClient from '@/api';
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
};

const actions: ActionTree<RecordState, any> = {
  async addShortageRecord({ commit }, record: BookShortage) {
    try {
      const response = await apiClient.post('/shortage/add', record);
      commit('ADD_SHORTAGE_RECORD', response.data);
    } catch (error) {
      console.error('Failed to add shortage record:', error);
      throw error;
    }
  },
  async fetchShortageRecords({ commit }) {
    try {
      const response = await apiClient.get('/shortage/list');
      commit('SET_SHORTAGE_RECORDS', response.data.shortages);
    } catch (error) {
      console.error('Failed to fetch shortage records:', error);
      throw error;
    }
  },
};

const shortageModule: Module<RecordState, any> = {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};

export default shortageModule;