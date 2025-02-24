import { Commit } from 'vuex';
import { Reader, ReaderList } from './types';
import apiClient from '@/api';

export default {
  namespaced: true,
  state(): { readers: ReaderList } {
    return {
      readers: []
    };
  },
  getters: {
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
  },
  actions: {
    async getUserInfo({ commit }: { commit: Commit }, { all, readerId }: { all: boolean, readerId?: number }): Promise<void> {
      try {
        if (all) {
          const response = await apiClient.get('/user/query');
          commit('SET_READERS', response.data.users);
        } else if (readerId !== undefined) {
          const response = await apiClient.get(`/user/query?reader_id=${readerId}`);
          commit('SET_READERS', [response.data.users]);
        }
      } catch (error) {
        console.error('Failed to fetch user info:', error);
        throw error;
      }
    },
    async register({ commit }: { commit: Commit }, reader: Reader): Promise<void> {
      try {
        const response = await apiClient.post('/user/register', reader);
        commit('ADD_READER', response.data);
      } catch (error) {
        console.error('Failed to register user:', error);
        throw error;
      }
    },
    async login({ commit }: { commit: Commit }, credentials: { user_id: string, password: string }): Promise<boolean> {
      try {
        const response = await apiClient.post('/user/login', credentials);
        return response.data.success;
      } catch (error) {
        console.error('Failed to login:', error);
        return false;
      }
    },
    async changeUserInfo({ commit }: { commit: Commit }, reader: Reader): Promise<void> {
      try {
        const response = await apiClient.put(`/user/update_balance`, reader);
        commit('UPDATE_READER', response.data);
      } catch (error) {
        console.error('Failed to change user info:', error);
        throw error;
      }
    }
  }
};