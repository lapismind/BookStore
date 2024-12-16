import { Book,BookList } from '@/store/modules/types';

export default {
  namespaced: true,
  state() {
    return {
      books: [
        {
          book_id: 1,
          title: "Java Programming",
          author: "xyz",
          publication_date: new Date("2020-05-01"),
          price: 39.99,
          publisher: "TechBooks",
          keywords: "Java, programming, technology",
          total_stock: 150,
          supplier: "Tech Supplier Ltd.",
          series_id: 2,
        },
        {
          book_id: 2,
          title: "编译原理",
          author: "hwq",
          publication_date: new Date("2020-06-01"),
          price: 20.0,
          publisher: "TechBooks",
          keywords: "humor, shabby",
          total_stock: 10,
          supplier: "Tech Supplier Ltd.",
          series_id: 4,
        },
      ] as BookList
    };
  },
  getters: {
    getBookById: (state: { books: BookList }) => (bookId: number) => {
      return state.books.find((book: Book) => book.book_id === bookId);
    },
  },
};