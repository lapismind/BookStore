<template>
  <div class="reader">
    <div class="reader-header">
      <img src="@/assets/user.svg" alt="我是头像" class="reader-avatar" />
    </div>
    <p>UID：{{ reader.reader_id }}</p>
    <p>{{ reader.user_id }}</p>
    <p>我的余额：{{ (Number(reader.balance)).toFixed(2) }}</p>
    <p>信用等级：{{ reader.credit_level }}</p>

    <div class="options">
      <a href="javascript:void(0);" class="option" @click="handleProfile">
        个人中心
      </a>
      <a href="javascript:void(0);" class="option" @click="handleOrders">
        我的订单
      </a>
      <a href="javascript:void(0);" class="option" @click="handleRecharge">
        余额充值
      </a>
      <hr class="divider">
      <a href="javascript:void(0);" class="option" @click="handleLogout">
        退出登录
      </a>
    </div>
    <!-- MyOrder 弹窗 -->
    <MyOrder :visible="isMyOrderModalVisible" :reader="reader" @close="isMyOrderModalVisible = false" />
    <!-- BuyModal 弹窗 -->
    <BuyModal v-if="selectedBook" :visible="isBuyModalVisible" :book="selectedBook" :reader="reader" @cancel="isBuyModalVisible = false" @add-order="addOrder" @update-reader="handleUpdateReader" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { defineProps, defineEmits } from 'vue';
import MyOrder from "@/components/MyOrder.vue";
import BuyModal from "@/components/BuyModal.vue";
import { Reader, Book } from '@/store/modules/types';
import Order from "@/store/modules/order";
import store from "@/store";
import order from "@/store/modules/order";

const props = defineProps<{ reader: Reader }>();

const emit = defineEmits(['update-reader']);

const isMyOrderModalVisible = ref(false);
const isBuyModalVisible = ref(false);
const selectedBook = ref<Book | null>(null);

const handleProfile = () => {
  // 处理个人中心逻辑
};

const handleOrders = () => {
  isMyOrderModalVisible.value = true;
};

const handleRecharge = () => {
  // 处理余额充值逻辑
};

const handleLogout = () => {
  const isConfirmed = confirm("真退吗哥？");
  if (isConfirmed) {
    window.location.href = '/home';
  }
};

const addOrder = async (order: typeof Order) => {
  try {
    await store.dispatch('order/addOrder', order);
    console.log('Order added successfully');
  } catch (error) {
    console.error('Failed to add order:', error);
  }
};

const handleUpdateReader = (updatedReader: Reader) => {
  emit('update-reader', updatedReader);
};
</script>

<style scoped>
.reader {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  color: #333;
}

.reader-header img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.reader p {
  font-size: 16px;
  line-height: 1.5;
}

.options {
  margin-top: 20px;
}

.option {
  display: block;
  margin-bottom: 10px;
  color: #007bff;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.3s ease;
}

.option:hover {
  color: #0056b3;
}
.divider {
  border: 0;
  height: 1px;
  background-color: #e0e0e0;
  margin: 10px 0;
}
</style>