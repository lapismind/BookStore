
export default {
  namespaced: true,
  state() {
    return {
      books: [
        {
          book_id: 1,
          title: "Java Programming",
          publication_date: "2020-05-01",
          price: 39.99,
          author: "xyz",
          publisher: "TechBooks",
          keywords: "Java, programming, technology",
          total_stock: 150,
          supplier: "Tech Supplier Ltd.",
          series_id: 2,
        },
        {
          book_id: 2,
          title: "编译原理",
          publication_date: "2020-06-01",
          price: 20.0,
          author: "hwq",
          publisher: "TechBooks",
          keywords: "humor, shabby",
          total_stock: 10,
          supplier: "Tech Supplier Ltd.",
          series_id: 4,
        },
      ]
    };
  },
};