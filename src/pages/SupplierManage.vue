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

  <div class="supplier-manage">
    <h2>供应商管理</h2>

    <!-- 新增供应商表单 -->
    <form @submit.prevent="addSupplier" class="supplier-form">
      <div class="form-group">
        <label for="name">名称:</label>
        <input type="text" id="name" v-model="newSupplier.name" required />
      </div>
      <div class="form-group">
        <label for="supplyInfo">供应信息:</label>
        <input type="text" id="supplyInfo" v-model="newSupplier.supply_info" required />
      </div>
      <button type="submit" class="action-button">新增</button>
    </form>

    <!-- 供应商列表 -->
    <table>
      <thead>
      <tr>
        <th>供应商ID</th>
        <th>名称</th>
        <th>供应信息</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="supplier in suppliers" :key="supplier.supplier_id">
        <td>{{ supplier.supplier_id }}</td>
        <td>{{ supplier.name }}</td>
        <td>{{ supplier.supply_info }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import type { Supplier } from '@/store/modules/types';

const store = useStore();

const newSupplier = ref<Supplier>({
  supplier_id: 0,
  name: '',
  supply_info: '',
});

const suppliers = computed(() => store.getters['supplier/suppliers']);

onMounted(async () => {
  await store.dispatch('supplier/fetchSuppliers');
});

const addSupplier = async () => {
  try {
    await store.dispatch('supplier/addSupplier', newSupplier.value);
    newSupplier.value = {
      supplier_id: 0,
      name: '',
      supply_info: '',
    };
  } catch (error) {
    console.error('Failed to add supplier:', error);
  }
};
</script>

<style scoped>
.supplier-manage {
  padding: 20px;
}

.supplier-form {
  margin-bottom: 20px;
}

.supplier-form .form-group {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.supplier-form .form-group label {
  margin-right: 10px;
}

.supplier-form .form-group input {
  flex: 1;
  padding: 8px;
  box-sizing: border-box;
}

.supplier-form .action-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.supplier-form .action-button:hover {
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