<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <span class="close" @click="$emit('close')">&times;</span>
      <h2>搜索订单信息</h2>
      <form @submit.prevent="searchOrder">
        <div>
          <label for="orderId">订单ID:</label>
          <input type="text" v-model="searchQuery.orderId" required />
        </div>
        <button type="submit" class="action-button">搜索</button>
      </form>
      <div v-if="order">
        <h3>订单信息</h3>
        <p>订单ID: {{ order.order_id }}</p>
        <p>读者ID: {{ order.reader_id }}</p>
        <p>书籍ID: {{ order.book_id }}</p>
        <p>系列ID: {{ order.series_id }}</p>
        <p>数量: {{ order.quantity }}</p>
        <p>价格: ¥{{ order.price }}</p>
        <p>订单日期: {{ order.order_date }}</p>
        <p>送货地址: {{ order.shipping_address }}</p>
        <p>支付状态: {{ order.if_paid ? '已支付' : '未支付' }}</p>
        <p>订单状态: {{ order.status }}</p>
      </div>
      <div v-else>
        <p>未找到订单。</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import type { Order } from '@/store/modules/types';

const props = defineProps<{ visible: boolean }>();
const store = useStore();

const searchQuery = ref({
  orderId: '',
});

const order = computed<Order | null>(() => {
  const id = parseInt(searchQuery.value.orderId, 10);
  if (!isNaN(id)) {
    return store.getters['order/getOrderById'](id);
  }
  return null;
});

const searchOrder = () => {
  // Trigger the computed property to update
  order.value;
};
</script>

<style scoped>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
}

.close {
  float: right;
  font-size: 24px;
  cursor: pointer;
}

.action-button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.action-button:hover {
  background-color: #0056b3;
}
</style>