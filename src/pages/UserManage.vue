<template>
  <div>
    <div class="nav-container">
      <router-link to="/book-list" class="nav-link">
        <img src="@/assets/bookList.svg" alt="书籍列表" class="icon" />
        <span class="nav-text">书籍列表</span>
      </router-link>
      <router-link to="/book-manage" class="nav-link">
        <img src="@/assets/bookManage.svg" alt="库存管理" class="icon" />
        <span class="nav-text">库存管理</span>
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
    <div class="user-list">
      <table>
        <thead>
        <tr>
          <th>Reader ID</th>
          <th>User ID</th>
          <th>Address</th>
          <th>Balance</th>
          <th>Credit Level</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="reader in paginatedReaders" :key="reader.reader_id">
          <td>{{ reader.reader_id }}</td>
          <td>{{ reader.user_id }}</td>
          <td>{{ reader.address }}</td>
          <td>{{ reader.balance }}</td>
          <td>{{ reader.credit_level }}</td>
        </tr>
        </tbody>
      </table>
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
        <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const currentPage = ref(1);
const itemsPerPage = 10;

const fetchReaders = () => {
  store.dispatch('user/fetchReaders');
};

const readers = computed(() => store.state.user.readers);

const totalPages = computed(() => Math.ceil(readers.value.length / itemsPerPage));

const paginatedReaders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return readers.value.slice(start, end);
});

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

watch(readers, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value;
  }
});

fetchReaders();
</script>

<style scoped>
.nav-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: center;
}

.nav-link {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #333;
}

.icon {
  width: 40px;
  height: 40px;
}

.nav-text {
  display: none;
  position: absolute;
  bottom: -40px;
  background-color: #fff;
  color: rgba(51, 51, 51, 0.58);
  padding: 5px 10px;
  border-radius: 30%;
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-link:hover .nav-text {
  display: block;
}

.nav-link:active .icon {
  filter: invert(100%);
}

.user-list {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}
</style>