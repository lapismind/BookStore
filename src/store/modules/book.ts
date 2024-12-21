import { Book, BookList } from '@/store/modules/types';
import axios from 'axios';
import { ActionContext } from 'vuex';

interface State {
  books: BookList;
}

export default {
  namespaced: true,
  state() {
    return {
      books: [] as BookList,
    };
  },
  getters: {
    getBookById: (state: State) => (bookId: string) => {
      return state.books.find((book: Book) => book.book_id === bookId);
    },
    getAllBooks: (state: State) => {
      return state.books;
    },
    searchBooks: (state: State) => (query: { id?: string, title?: string, publisher?: string, keywords?: string, author?: string }) => {
      return state.books.filter((book: Book) => {
        return (!query.id || book.book_id.includes(query.id)) &&
          (!query.title || book.title.includes(query.title)) &&
          (!query.publisher || book.publisher.includes(query.publisher)) &&
          (!query.keywords || book.keywords.includes(query.keywords)) &&
          (!query.author || book.author.includes(query.author));
      });
    },
  },
  mutations: {
    setBooks(state: State, books: BookList) {
      state.books = books;
    },
    addBook(state: State, book: Book) {
      state.books.push(book);
    },
    deleteBook(state: State, bookId: string) {
      const index = state.books.findIndex((book: Book) => book.book_id === bookId);
      state.books.splice(index, 1);
    },
    updateBook(state: State, book: Book) {
      const index = state.books.findIndex((b: Book) => b.book_id === book.book_id);
      state.books.splice(index, 1, book);
    },
  },
  actions: {
    async fetchBookInfo({ commit }: ActionContext<State, unknown>) {
      try {
        const response = await axios.get('/book/get_book_info');
        commit('setBooks', response.data);
      } catch (error) {
        console.error('Failed to fetch book info:', error);
        throw error;
      }
    },
    async addBook({ commit }: ActionContext<State, unknown>, book: Book) {
      try {
        await axios.post('/book/add_book', book);
        commit('addBook', book);
      } catch (error) {
        console.error('Failed to add book:', error);
        throw error;
      }
    },
  },
};