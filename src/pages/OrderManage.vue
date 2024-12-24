<template>
  <div>
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
    <div class="order-list">
      <table v-if="orders.length > 0">
        <thead>
        <tr>
          <th>订单ID</th>
          <th>书籍ID</th>
          <th>用户ID</th>
          <th>数量</th>
          <th>价格</th>
          <th>订单时间</th>
          <th>收货地址</th>
          <th>状态</th>
          <th>待发货</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="order in sortedOrders" :key="order.order_id">
          <td>{{ order.order_id }}</td>
          <td>{{ order.book_id }}</td>
          <td>{{ order.reader_id }}</td>
          <td>{{ order.quantity }}</td>
          <td>{{ order.price }}</td>
          <td>{{ formatDate(new Date(order.order_date)) }}</td>
          <td>{{ order.shipping_address }}</td>
          <td>{{ order.status }}</td>
          <td>
            <button v-if="order.status === 'pending'" @click="shipOrder(order.order_id)" class="action-button">发货</button>
          </td>
        </tr>
        </tbody>
      </table>
      <div v-else class="no-data">没有订单数据</div>
      <div class="pagination" v-if="orders.length > 0">
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
import { Order } from '@/store/modules/types';

const store = useStore();
const currentPage = ref(1);
const itemsPerPage = 10;

const fetchOrders = () => {
  store.dispatch('order/fetchOrders');
};

const orders = computed(() => store.state.order.orders);

const totalPages = computed(() => Math.ceil(orders.value.length / itemsPerPage));

const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return orders.value.slice(start, end);
});

const sortedOrders = computed(() => {
  return paginatedOrders.value.sort((a: Order, b: Order) => {
    if (a.status === 'pending' && b.status !== 'pending') return -1;
    if (a.status !== 'pending' && b.status === 'pending') return 1;
    return 0;
  });
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

const shipOrder = (orderId: number) => {
  store.dispatch('order/shipOrder', orderId);
};

const formatDate = (date: Date): string => {
  return date.toLocaleDateString();
};

watch(orders, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value;
  }
});

fetchOrders();
</script>

<style scoped>
.order-list {
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

.no-data {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  color: #888;
}
</style>