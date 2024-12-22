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
      <span class="nav-text">搜索</span>
    </router-link>
    <router-link to="/home" class="nav-link">
      <img src="@/assets/exit.svg" alt="退出管理页面" class="icon" />
      <span class="nav-text">退出管理页面</span>
    </router-link>
  </div>
  <div class="book-manage">
    <div class="button-group">
      <button @click="showShortageModal = true" class="action-button">缺货表</button>
      <button @click="showProcurementModal = true" class="action-button">采购单</button>
    </div>
    <div v-if="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="books.length === 0 && !loading">没有书籍数据。</div>
    <table v-if="books.length > 0">
      <thead>
      <tr>
        <th>书籍ID</th>
        <th>书名</th>
        <th>作者</th>
        <th>供应商</th>
        <th>库存数量</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="book in books" :key="book.book_id">
        <td>{{ book.book_id }}</td>
        <td>{{ book.title }}</td>
        <td>{{ book.author }}</td>
        <td>{{ book.supplier }}</td>
        <td>{{ book.total_stock }}</td>
      </tr>
      </tbody>
    </table>
    <ShortageRecord
      :visible="showShortageModal"
      @close="showShortageModal = false"
    />
    <ProcurementRecord
      :visible="showProcurementModal"
      @close="showProcurementModal = false"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex';
import ShortageRecord from "@/components/ShortageRecord.vue";
import ProcurementRecord from "@/components/ProcurementRecord.vue";


export default {
  name: "BookManage",
  components: {
    ShortageRecord,
    ProcurementRecord,
  },
  data() {
    return {
      loading: false,
      error: null,
      showShortageModal: false,
      showProcurementModal: false,
      page: 1,
      size: 3,
    };
  },
  computed: {
    ...mapState('book', ['books']),
  },
};
</script>

<style scoped>
.book-manage {
  padding: 20px;
}

.book-manage table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.book-manage th,
.book-manage td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.book-manage th {
  background-color: #f2f2f2;
}

.book-manage .error {
  color: red;
}

.button-group {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
</style>