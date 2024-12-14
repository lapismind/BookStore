<template>
  <div v-if="book" class="book-details">
    <!-- 书名 -->
    <div class="book-title">{{ book.title }}</div>

    <!-- 书籍信息，包括出版时间、作者、丛书号 -->
    <div class="book-info">
      <span class="book-info-item">{{ book.publication_date }}</span>
      <span class="book-info-item">{{ book.author }}</span>
      <span class="book-info-item">丛书号: {{ book.series_id }}</span>
    </div>

    <!-- 关键字 -->
    <div class="book-keywords">
      <span>关键字: {{ book.keywords }}</span>
    </div>

    <!-- 价格 -->
    <div class="book-price">
      <span>价格: ¥{{ book.price }}</span>
    </div>

    <!-- 购买按钮 -->
    <div>
      <button @click="showBuyModal = true">购买</button>
      <BuyModal
        :visible="showBuyModal"
        :book="book"
        :reader="reader"
        @update-reader="updateReader"
        @cancel="showBuyModal = false"
      />
    </div>
  </div>
</template>

<script>
import BuyModal from "@/components/BuyModal.vue";

export default {
  components: {
    BuyModal,
  },
  props: {
    book: Object, // 从父组件接收 book 数据
    reader: Object, // 从父组件接收 userBalance 数据
  },
  data() {
    return {
      showBuyModal: false, // 控制弹窗显示
    };
  },
  methods: {
    handlePurchase(order) {
      alert(`购买成功！\n余额: ¥${order.remainingBalance}`);
      this.showBuyModal = false; // 关闭弹窗
    },
  },
};
</script>

<style scoped>
.book-details {
  display: flex;
  flex-direction: column;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 300px;
  background-color: #f9f9f9;
}

.book-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.book-info {
  font-size: 12px;
  color: #888;
  margin-bottom: 10px;
}

.book-info-item {
  margin-right: 15px;
}

.book-keywords {
  font-size: 14px;
  color: #555;
  margin-bottom: 10px;
}

.book-price {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
}

.buy-button-container {
  display: flex;
  justify-content: flex-end;
}

.buy-button {
  padding: 8px 15px;
  font-size: 14px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.buy-button:hover {
  background-color: #0056b3;
}
</style>
