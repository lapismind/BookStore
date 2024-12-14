<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <h2 class="modal-header">采购单</h2>
      <table>
        <tr v-for="book in soldBooks" :key="book.book_id">
          <td>{{ book.title }}</td>
          <td>
            <input
              type="number"
              v-model.number="book.purchaseQuantity"
              min="1"
            />
          </td>
        </tr>
      </table>
      <div class="modal-actions">
        <button @click="$emit('close')">关闭</button>
        <button @click="generatePurchaseOrder">生成采购单</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RestockForm",
  props: {
    visible: Boolean,
  },
  data() {
    return {
      books: [], // 所有书籍的列表
      soldBooks: [], // 状态为 sold 的书籍列表
      loading: false,
      error: null,
    };
  },
  mounted() {
    this.fetchBooks();
  },
  methods: {
    fetchBooks() {
      this.loading = true;
      this.error = null;
      // 模拟 API 请求
      setTimeout(() => {
        this.loading = false;
        // 模拟书籍数据
        this.books = [
          {
            book_id: 1,
            title: "Java Programming",
            publication_date: "2020-05-01",
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
            publication_date: "2020-06-01",
            price: 20.0,
            publisher: "TechBooks",
            keywords: "compiler, programming, theory",
            total_stock: 10,
            supplier: "Tech Supplier Ltd.",
            series_id: 4,
          },
          // ... 更多书籍
        ];

        // 模拟库存数据
        const soldInventory = [
          { book_id: 1, status: "sold" },
          { book_id: 2, status: "sold" },
          // ... 更多 sold 状态的书籍
        ];

        // 过滤出状态为 sold 的书籍
        this.soldBooks = soldInventory
          .filter((inv) => inv.status === "sold")
          .map((inv) => {
            return this.books.find((book) => book.book_id === inv.book_id);
          })
          .map((book) => ({
            ...book,
            purchaseQuantity: 0, // 初始化采购数量为0
          }));
      }, 1000); // 1秒后模拟响应
    },
    generatePurchaseOrder() {
      // 在这里添加生成采购单的逻辑
      console.log("生成的采购单:", this.soldBooks);
      this.$emit("close"); // 关闭弹窗
    },
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  width: 600px;
  border-radius: 8px;
}

.modal-header {
  font-size: 24px;
  margin-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-left: 10px;
}

button:hover {
  background-color: #0056b3;
}
</style>
