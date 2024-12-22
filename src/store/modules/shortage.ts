import { GetterTree, MutationTree, ActionTree } from 'vuex';
import { BookShortage } from '@/store/modules/types';
import axios from 'axios';

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
      await axios.post('/shortage/add', record);
      commit('ADD_SHORTAGE_RECORD', record);
    } catch (error) {
      console.error('Failed to add shortage record:', error);
      throw error;
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