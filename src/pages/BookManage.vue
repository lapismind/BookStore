<template>
  <div class="nav-container">
    <router-link to="/book-manage" class="nav-link">
      <img src="../assets/bookManage.svg" alt="书籍列表" class="icon" />
      <span class="nav-text">供书目录管理</span>
    </router-link>
    <router-link to="/procurement-manage" class="nav-link">
      <img src="../assets/ProcurementManage.svg" alt="库存管理" class="icon" />
      <span class="nav-text">采购管理</span>
    </router-link>
    <router-link to="/user-manage" class="nav-link">
      <img src="@/assets/userManage.svg" alt="用户管理" class="icon" />
      <span class="nav-text">用户管理</span>
    </router-link>
    <router-link to="/order-manage" class="nav-link">
      <img src="@/assets/orderManage.svg" alt="用户订单管理" class="icon" />
      <span class="nav-text">用户订单管理</span>
    </router-link>
    <router-link to="/supplier-manage" class="nav-link">
      <img src="@/assets/supplierManage.svg" alt="供应商管理" class="icon" />
      <span class="nav-text">供应商管理</span>
    </router-link>
    <router-link to="/search" class="nav-link">
      <img src="@/assets/search.svg" alt="搜索" class="icon" />
      <span class="nav-text">全局搜索</span>
    </router-link>
    <router-link to="/home" class="nav-link">
      <img src="@/assets/exit.svg" alt="退出管理页面" class="icon" />
      <span class="nav-text">退出管理页面</span>
    </router-link>
  </div>
  <div class="book-list-container">
    <table>
      <thead>
      <tr>
        <th>书籍ID</th>
        <th>书名</th>
        <th>作者</th>
        <th>出版日期</th>
        <th>价格</th>
        <th>出版社</th>
        <th>关键字</th>
        <th>库存数量</th>
        <th>供应商</th>
        <th>丛书号</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="book in paginatedBooks" :key="book.book_id">
        <td>{{ book.book_id }}</td>
        <td>{{ book.title }}</td>
        <td>{{ book.author }}</td>
        <td>{{ book.publication_date }}</td>
        <td>{{ book.price }}</td>
        <td>{{ book.publisher }}</td>
        <td>{{ book.keywords }}</td>
        <td>{{ book.total_stock }}</td>
        <td>{{ book.supplier }}</td>
        <td>{{ book.series_id }}</td>
      </tr>
      </tbody>
    </table>
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
      <button @click="showAddBookModal = true" class="action-button">新书入库</button>
    </div>
    <AddBookModal
      :visible="showAddBookModal"
      @close="showAddBookModal = false"
      @add-book="addBook"
    />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import AddBookModal from '@/components/AddBookModal.vue';

export default {
  components: {
    AddBookModal,
  },
  data() {
    return {
      showAddBookModal: false,
      currentPage: 1,
      pageSize: 10,
    };
  },
  computed: {
    ...mapState('book', ['books']),
    totalPages() {
      return Math.ceil(this.books.length / this.pageSize);
    },
    paginatedBooks() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.books.slice(start, end);
    },
  },
  methods: {
    ...mapActions('book', ['fetchBooks', 'addBook']),
    async addBook(newBook) {
      try {
        await this.$store.dispatch('book/addBook', newBook);
        await this.fetchBooks();
        newBook.supplier.forEach(async (supplierName) => {
          const supplier = {
            supplier_id: Date.now(),
            name: supplierName,
            book_list: [{ book_id: newBook.book_id, series_id: newBook.series_id }],
          };
          await this.$store.dispatch('supplier/addSupplier', supplier);
        });
      } catch (error) {
        console.error('Failed to add book:', error);
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
  },
  async mounted() {
    await this.fetchBooks();
  },
};
</script>

<style scoped>
.book-list-container {
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

.action-button {
  margin-left: 10px;
}
</style>