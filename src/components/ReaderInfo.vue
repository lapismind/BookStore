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
  </div>
  <!-- Independent Image Modal -->
  <div v-if="isImageModalVisible" class="modal">
    <div class="modal-content">
      <span class="close" @click="isImageModalVisible = false">&times;</span>
      <img src="@/assets/charge.jpg" alt="New Image" class="modal-image" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { defineProps, defineEmits } from 'vue';
import MyOrder from "@/components/MyOrder.vue";
import { Reader, Book } from '@/store/modules/types';

const props = defineProps<{ reader: Reader }>();

const emit = defineEmits(['update-reader']);

const isMyOrderModalVisible = ref(false);
const isImageModalVisible = ref(false);

const handleProfile = () => {
  // 处理个人中心逻辑
};

const handleOrders = () => {
  isMyOrderModalVisible.value = true;
};

const handleRecharge = () => {
  isImageModalVisible.value = true;
};

const handleLogout = () => {
  const isConfirmed = confirm("确认退出？");
  if (isConfirmed) {
    window.location.href = '/home';
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

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: #fefefe;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 500px;
  border-radius: 8px;
  position: relative;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.modal-image {
  width: 100%;
  height: auto;
}
</style>