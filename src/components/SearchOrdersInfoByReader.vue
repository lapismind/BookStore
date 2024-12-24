<template>
  <div>
    <button @click="openModal" class="action-button">查询订单</button>
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-button" @click="closeModal"></button>
        <form @submit.prevent="searchOrders">
          <div class="form-group">
            <label for="readerId">Reader ID:</label>
            <input type="text" id="readerId" v-model="readerId" />
          </div>
        </form>
        <div v-if="orders.length > 0">
          <h2>订单信息:</h2>
          <ul>
            <li v-for="order in orders" :key="order.order_id">
              <p>订单ID: {{ order.order_id }}</p>
              <p>书籍ID: {{ order.book_id }}</p>
              <p>订单数量: {{ order.quantity }}</p>
              <p>价格: ¥{{ order.price }}</p>
              <p>订单日期: {{ formatDate(new Date(order.order_date)) }}</p>
              <p>送货地址: {{ order.shipping_address }}</p>
              <p>订单状态: {{ order.status }}</p>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No orders found.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useStore } from 'vuex';
import { Order } from '@/store/modules/types';

const store = useStore();

const readerId = ref('');
const orders = ref<Order[]>([]);

const searchOrders = () => {
  const id = parseInt(readerId.value, 10);
  if (!isNaN(id)) {
    orders.value = store.getters['order/getOrdersByReaderId'](id);
  }
};

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const formatDate = (date: Date): string => {
  return date.toLocaleDateString();
};
</script>

<style scoped>
.modal-overlay {
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
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 500px;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.form-group label {
  margin-right: 10px;
}

.form-group input {
  flex: 1;
  padding: 8px;
  box-sizing: border-box;
}
</style>