<template>
  <div class="nav-container" >
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

  <div class="search-page" style="overflow: hidden;">
    <div class="button-grid">
      <div class="button-cell">
        <img src="@/assets/searchBook.svg" alt="Search Book" @click="showSearchBookModal = true" class="search-button" />
      </div>
      <div class="button-cell">
        <img src="@/assets/searchOrder.svg" alt="Search Order" @click="showSearchOrderModal = true" class="search-button" />
      </div>
      <div class="button-cell">
        <img src="@/assets/searchSupplier.svg" alt="Search Supplier" @click="showSearchSupplierModal = true" class="search-button" />
      </div>
      <div class="button-cell">
        <img src="@/assets/searchReader.svg" alt="Search Reader" @click="showSearchReaderModal = true" class="search-button" />
      </div>
    </div>

    <SearchBookInfo :visible="showSearchBookModal" @close="showSearchBookModal = false" />
    <SearchOrderInfo :visible="showSearchOrderModal" @close="showSearchOrderModal = false" />
    <SearchSupplierInfo :visible="showSearchSupplierModal" @close="showSearchSupplierModal = false" />
    <SearchReaderInfo :visible="showSearchReaderModal" @close="showSearchReaderModal = false" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SearchBookInfo from '@/components/SearchBookInfo.vue';
import SearchOrderInfo from '@/components/SearchOrderInfo.vue';
import SearchSupplierInfo from '@/components/SearchSupplierInfo.vue';
import SearchReaderInfo from '@/components/SearchReaderInfo.vue';

const showSearchBookModal = ref(false);
const showSearchOrderModal = ref(false);
const showSearchSupplierModal = ref(false);
const showSearchReaderModal = ref(false);
</script>

<style scoped>
.search-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.button-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.button-cell {
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-button {
  width: 150px;
  height: 150px;
  cursor: pointer;
  transition: box-shadow 0.3s ease;
  margin: 30px;
}

.search-button:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>