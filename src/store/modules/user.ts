// store/modules/user.ts
import { Commit, Dispatch } from 'vuex';
import { Reader } from './types';

//模拟一下先
export default {
  namespaced: true,
  state(): { reader: Reader } {
    return {
      reader: {
        reader_id: 101,
        user_id: "user123",
        address: "515",
        balance: 150.00,
        credit_level: 3
      }
    };
  },
  getters: {
    getCurrentReader(state: { reader: Reader }): Reader {
      return state.reader;
    },
    getReaderId(state: { reader: Reader }): number {
      return state.reader.reader_id;
    },
    getUserId(state: { reader: Reader }): string {
      return state.reader.user_id;
    },
    getReaderAddress(state: { reader: Reader }): string {
      return state.reader.address;
    },
    getReaderBalance(state: { reader: Reader }): number {
      return state.reader.balance;
    },
    getReaderCreditLevel(state: { reader: Reader }): number {
      return state.reader.credit_level;
    }
  },
  mutations: {
    SET_READER(state: { reader: Reader }, readerData: Reader): void {
      state.reader = readerData;
    }
  },
  actions: {
    fetchReader({ commit }: { commit: Commit }): void {
      setTimeout(() => {
        commit('SET_READER', {
          reader_id: 101,
          user_id: "user123",
          address: "515",
          balance: 150.0,
          credit_level: 3
        });
      }, 1000);
    }
  }
};