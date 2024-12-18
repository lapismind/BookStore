// store/modules/user.ts
import { Commit, Dispatch } from 'vuex';
import { Reader, ReaderList } from './types';

export default {
  namespaced: true,
  state(): { readers: ReaderList } {
    return {
      readers: []
    };
  },
  getters: {
    getAllReaders(state: { readers: ReaderList }): ReaderList {
      return state.readers;
    },
    getReaderById: (state: { readers: ReaderList }) => (readerId: number): Reader | undefined => {
      return state.readers.find(reader => reader.reader_id === readerId);
    }
  },
  mutations: {
    SET_READERS(state: { readers: ReaderList }, readers: ReaderList): void {
      state.readers = readers;
    },
    ADD_READER(state: { readers: ReaderList }, reader: Reader): void {
      state.readers.push(reader);
    },
    UPDATE_READER(state: { readers: ReaderList }, updatedReader: Reader): void {
      const index = state.readers.findIndex(reader => reader.reader_id === updatedReader.reader_id);
      if (index !== -1) {
        state.readers.splice(index, 1, updatedReader);
      }
    },
    DELETE_READER(state: { readers: ReaderList }, readerId: number): void {
      state.readers = state.readers.filter(reader => reader.reader_id !== readerId);
    }
  },
  actions: {
    fetchReaders({ commit }: { commit: Commit }): void {
      // Simulate an API call
      setTimeout(() => {
        const readers: ReaderList = [
          {
            reader_id: 101,
            user_id: "user123",
            address: "515",
            balance: 150.00,
            credit_level: 3
          },
          {
            reader_id: 102,
            user_id: "user456",
            address: "123",
            balance: 200.00,
            credit_level: 4
          }
        ];
        commit('SET_READERS', readers);
      }, 1000);
    },
    addReader({ commit }: { commit: Commit }, reader: Reader): void {
      commit('ADD_READER', reader);
    },
    updateReader({ commit }: { commit: Commit }, reader: Reader): void {
      commit('UPDATE_READER', reader);
    },
    deleteReader({ commit }: { commit: Commit }, readerId: number): void {
      commit('DELETE_READER', readerId);
    }
  }
};