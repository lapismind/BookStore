<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <h2>我的订单</h2>
      <ul>
        <li v-for="(order, index) in orders" :key="index" class="order-item" style="text-align: left;">
          <div><strong>订单ID:</strong> {{ order.order_id }}</div>
          <div><strong>下单数量:</strong> {{ order.quantity }}</div>
          <div><strong>价格:</strong> ¥{{ order.price }}</div>
          <div><strong>订单时间:</strong> {{ formatDate(new Date(order.order_date)) }}</div>
          <div><strong>收货地址:</strong> {{ order.shipping_address }}</div>
          <div><strong>状态:</strong> {{ order.status }}</div>
          <button v-if="order.status === 'shipped'" @click="receiveOrder(order.order_id)" class="action-button">收货</button>
        </li>
      </ul>
      <button @click="closeModal">关闭</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, computed } from "vue";
import { useStore } from 'vuex';
import { Order, Reader } from "@/store/modules/types";

const props = defineProps<{
  visible: boolean;
  reader: Reader;
}>();

const emit = defineEmits(['close']);

const store = useStore();

const orders = computed<Order[]>(() => store.getters['order/getOrdersByReaderId'](props.reader.reader_id));

const closeModal = () => {
  emit('close');
};

const receiveOrder = async (orderId: number) => {
  try {
    await store.dispatch('order/receiveOrder', orderId);
  } catch (error) {
    console.error('Failed to receive order:', error);
  }
};

const formatDate = (date: Date): string => {
  return date.toLocaleDateString();
};

console.log(props.visible);
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
  max-height: 80vh;
  overflow-y: auto;
}
.order-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>