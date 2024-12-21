// store/modules/user.ts
import { Commit } from 'vuex';
import { Reader, ReaderList } from './types';
import axios from 'axios';

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
    },
    searchReaders: (state: { readers: ReaderList }) => (query: { readerId?: number, userId?: string }): ReaderList => {
      return state.readers.filter(reader => {
        return (query.readerId !== undefined && reader.reader_id === query.readerId) ||
          (query.userId !== undefined && reader.user_id === query.userId);
      });
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
    async getUserInfo({ commit }: { commit: Commit }, { all, readerId }: { all: boolean, readerId?: number }): Promise<void> {
      try {
        if (all) {
          const response = await axios.get('/user/get_user_info/all');
          commit('SET_READERS', response.data);
        } else if (readerId !== undefined) {
          const response = await axios.get(`/user/get_user_info/${readerId}`);
          commit('SET_READERS', [response.data]);
        }
      } catch (error) {
        console.error('Failed to fetch user info:', error);
        throw error;
      }
    },
    async register({ commit }: { commit: Commit }, reader: Reader): Promise<void> {
      try {
        await axios.post('/user/register', reader);
        commit('ADD_READER', reader);
      } catch (error) {
        console.error('Failed to register user:', error);
        throw error;
      }
    },
    async login({ commit }: { commit: Commit }, credentials: { user_id: string, password: string }): Promise<boolean> {
      try {
        const response = await axios.post('/user/login', credentials);
        return response.data.success;
      } catch (error) {
        console.error('Failed to login:', error);
        return false;
      }
    },
    async changeUserInfo({ commit }: { commit: Commit }, reader: Reader): Promise<void> {
      try {
        await axios.put(`/user/change_user_info/${reader.reader_id}`, reader);
        commit('UPDATE_READER', reader);
      } catch (error) {
        console.error('Failed to change user info:', error);
        throw error;
      }
    }
  }
};