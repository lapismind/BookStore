<template>
  <div v-if="book" class="book-details">
    <!-- 书名 -->
    <div class="book-title">{{ book.title }}</div>

    <!-- 书籍信息，包括出版时间、作者、丛书号 -->
    <div class="book-info">
      <span class="book-info-item">{{ book.publication_date }}</span>
      <span class="book-info-item">{{ book.author.join(', ') }}</span>
      <span class="book-info-item">丛书号: {{ book.series_id }}</span>
    </div>

    <!-- 关键字 -->
    <div class="book-keywords">
      <span>关键字: {{ book.keywords.join(', ') }}</span>
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

<script lang="ts">
import { defineComponent, ref } from 'vue';
import BuyModal from "@/components/BuyModal.vue";
import { Book, Reader } from '@/store/modules/types';

export default defineComponent({
  name: "BookDetails",
  components: {
    BuyModal,
  },
  props: {
    book: {
      type: Object as () => Book,
      required: true,
    },
    reader: {
      type: Object as () => Reader,
      default: () => ({
        reader_id: 1,
        user_id: '',
        address: '',
        balance: 0,
        credit_level: 0,
      }),
    },
  },
  emits: ['update-reader'],
  setup(props, { emit }) {
    const showBuyModal = ref(false);

    const updateReader = (updatedReader: Reader) => {
      emit('update-reader', updatedReader);
    };

    return {
      showBuyModal,
      updateReader,
    };
  },
});
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
</style>