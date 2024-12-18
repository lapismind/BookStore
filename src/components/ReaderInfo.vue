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
    <MyOrder :visible="isMyOrderModalVisible" :orders="orders" @close="isMyOrderModalVisible = false" />
    <!-- BuyModal 弹窗 -->
    <BuyModal v-if="selectedBook" :visible="isBuyModalVisible" :book="selectedBook" :reader="reader" @cancel="isBuyModalVisible = false" @add-order="addOrder" @update-reader="handleUpdateReader" />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import MyOrder from "@/components/MyOrder.vue";
import BuyModal from "@/components/BuyModal.vue";
import { Reader, Book } from '@/store/modules/types';

export default defineComponent({
  name: "ReaderInfo",
  components: {
    MyOrder,
    BuyModal,
  },
  props: {
    reader: {
      type: Object as PropType<Reader>,
      required: true,
    },
  },
  data() {
    return {
      isMyOrderModalVisible: false,
      isBuyModalVisible: false,
      selectedBook: null as Book | null,
      orders: [] as any[], // 根据实际情况调整类型
    };
  },
  methods: {
    handleProfile() {
      // 处理个人中心逻辑
    },
    handleOrders() {
      this.isMyOrderModalVisible = true;
    },
    handleRecharge() {
      // 处理余额充值逻辑
    },
    handleLogout() {
      const isConfirmed = confirm("真退吗哥？");
      if (isConfirmed) {
        this.$router.push('/home');
      }
    },
    addOrder(order: any) {
      this.orders.push(order);
    },
    handleUpdateReader(updatedReader: Reader) {
      this.$emit('update-reader', updatedReader);
    },
  },
});
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
  width: 100px; /* 根据需要调整图片大小 */
  height: 100px;
  border-radius: 50%; /* 圆形图片 */
  object-fit: cover; /* 确保图片内容适应圆形 */
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
   