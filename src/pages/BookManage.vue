<!-- BookManage.vue -->
<template>
  <div class="book-manage">
    <router-link to="/book-manage" class="nav-link">书籍库存管理</router-link> |
    <router-link to="/order-manage" class="nav-link">用户订单管理</router-link> |
    <router-link to="/home" class="nav-link">退出管理页面</router-link>
    <hr>
    <router-view></router-view>
    <div class="button-group">
      <button @click="showRestockModal = true" class="action-button">
        新增采购单
      </button>
      <button @click="showShortageModal = true" class="action-button">缺货记录</button>
      <button class="action-button">采购记录</button>
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
    <RestockForm
      :visible="showRestockModal"
      @close="showRestockModal = false"
    />
    <ShortageRecord
      :visible="showShortageModal"
      @close="showShortageModal = false"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex';
import RestockForm from "@/components/RestockForm.vue";
import ShortageRecord from "@/components/ShortageRecord.vue";

export default {
  name: "BookManage",
  components: {
    RestockForm,
    ShortageRecord,
  },
  data() {
    return {
      loading: false,
      error: null,
      showRestockModal: false,
      showShortageModal: false,
      page: 1,
      size: 3,
    };
  },
  computed: {
    ...mapState('book', ['books']),
  },
  mounted() {
    this.loading = true;
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  },
  methods: {
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
