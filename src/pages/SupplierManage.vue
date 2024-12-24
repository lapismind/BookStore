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

  <div class="supplier-manage">
    <div class="button-group">
      <button @click="showAddSupplierModal = true" class="action-button">新增供应商</button>
      <button @click="showSearchSupplierModal = true" class="action-button">搜索供应商信息</button>
    </div>

    <table>
      <thead>
      <tr>
        <th>供应商ID</th>
        <th>名称</th>
        <th>书籍列表</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="supplier in suppliers" :key="supplier.supplier_id">
        <td>{{ supplier.supplier_id }}</td>
        <td>{{ supplier.name }}</td>
        <td>
          <ul>
            <li v-for="book in supplier.book_list" :key="book.book_id">
              {{ book.book_id }} - {{ book.series_id }}
            </li>
          </ul>
        </td>
      </tr>
      </tbody>
    </table>

    <AddSupplier
      :visible="showAddSupplierModal"
      @close="showAddSupplierModal = false"
    />
    <SearchSupplierInfo
      :visible="showSearchSupplierModal"
      @close="showSearchSupplierModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import AddSupplier from '@/components/AddSupplier.vue';
import SearchSupplierInfo from '@/components/SearchSupplierInfo.vue';
import type { Supplier } from '@/store/modules/types';

const store = useStore();

const showAddSupplierModal = ref(false);
const showSearchSupplierModal = ref(false);

const suppliers = computed<Supplier[]>(() => store.getters['supplier/suppliers']);

onMounted(async () => {
  await store.dispatch('supplier/fetchSuppliers');
});
</script>

<style scoped>
.supplier-manage {
  padding: 20px;
}

.button-group {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.action-button {
  margin-right: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.action-button:hover {
  background-color: #0056b3;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table th, table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

table th {
  background-color: #f2f2f2;
}
</style>