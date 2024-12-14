<template>
  <div>
    <!-- 使用 v-for 渲染多本书籍 -->
    <BookDetails
      v-for="book in books"
      :key="book.book_id"
      :book="book"
      :reader="reader"
      @update-reader="updateReader"
    />
  </div>
</template>

<script>
import BookDetails from "@/components/BookDetails.vue";
import axios from "axios";

export default {
  components: {
    BookDetails,
  },
  data() {
    return {
      books: [], // Initializing the 'book' object, which will be populated later
      reader: null, // Adding a 'reader' object to hold user information
    };
  },
  mounted() {
    // Simulating the API response for books
    this.books = [
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
      // 添加更多书籍信息...
      {
        book_id: 2,
        title: "编译原理",
        publication_date: "2020-06-01",
        price: 20.0,
        author: "hwq",
        publisher: "TechBooks",
        keywords: "humor，shabby",
        total_stock: 10,
        supplier: "Tech Supplier Ltd.",
        series_id: 4,
      },
    ];

    // Simulating the reader (user) data
    this.reader = {
      reader_id: 101, // Unique reader ID
      user_id: "user123", // User identifier
      address: "515", // User's address
      balance: 150.0, // User's balance
      credit_level: 3, // User's credit level (e.g., 1-5 scale)
    };
  },
  methods: {
    updateReader(updatedReader) {
      this.reader = updatedReader;
    },
  },
};
</script>

<style scoped>
/* 页面样式，可以根据需求添加 */
</style>
