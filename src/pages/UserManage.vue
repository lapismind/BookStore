<template>
  <div>
    <div class="nav-container">
      <router-link to="/book-manage" class="nav-link">
        <img src="../assets/bookManage.svg" alt="图书管理" class="icon" />
        <span class="nav-text">图书管理</span>
      </router-link>
      <router-link to="/procurement-manage" class="nav-link">
        <img src="../assets/ProcurementManage.svg" alt="采购管理" class="icon" />
        <span class="nav-text">采购管理</span>
      </router-link>
      <router-link to="/user-manage" class="nav-link">
        <img src="@/assets/userManage.svg" alt="用户管理" class="icon" />
        <span class="nav-text">用户管理</span>
      </router-link>
      <router-link to="/order-manage" class="nav-link">
        <img src="@/assets/orderManage.svg" alt="订单管理" class="icon" />
        <span class="nav-text">订单管理</span>
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
        <img src="@/assets/exit.svg" alt="退出" class="icon" />
        <span class="nav-text">退出</span>
      </router-link>
    </div>
    <div class="button-group">
      <button @click="showUserRegisterModal = true" class="action-button">用户注册</button>
      <button @click="showUserSearchModal = true" class="action-button">用户查询</button>
    </div>
    <div class="user-list">
      <table>
        <thead>
        <tr>
          <th>用户ID</th>
          <th>用户昵称</th>
          <th>用户地址</th>
          <th>用户余额</th>
          <th>信用等级</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="reader in paginatedReaders" :key="reader.reader_id">
          <td>{{ reader.reader_id }}</td>
          <td>{{ reader.user_id }}</td>
          <td>{{ reader.address }}</td>
          <td>
            <input type="number" v-model="reader.balance" />
            <button @click="updateBalance(reader)">更新余额</button>
          </td>
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
    <RegisterUser :visible="showUserRegisterModal" @close="showUserRegisterModal = false" />
    <SearchReaderInfo :visible="showUserSearchModal" @close="showUserSearchModal = false" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useStore } from 'vuex';
import { Reader } from '@/store/modules/types';
import RegisterUser from '@/components/RegisterUser.vue';
import SearchReaderInfo from '@/components/SearchReaderInfo.vue';

const showUserRegisterModal = ref(false);
const showUserSearchModal = ref(false);

const store = useStore();
const currentPage = ref(1);
const itemsPerPage = 10;

const fetchReaders = () => {
  store.dispatch('user/getUserInfo', { all: true });
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

const updateBalance = (reader: Reader) => {
  store.dispatch('user/changeUserInfo', reader).then(() => {
    fetchReaders();
  });
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.button-group {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
</style>