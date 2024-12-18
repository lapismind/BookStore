<!-- BuyModal.vue -->
<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <h2 class="modal-header">订单详情</h2>
      <div class="book-info">
        <div>
          <strong>书名:</strong>
          <span class="book-title">{{ book.title }}</span>
        </div>
        <div><strong>出版日期:</strong> {{ book.publication_date }}</div>
        <div><strong>作者:</strong> {{ book.author }}</div>
        <div><strong>出版商:</strong> {{ book.publisher }}</div>
        <div><strong>简介:</strong> 暂无</div>
        <div><strong>价格:</strong> ¥{{ book.price }}</div>
      </div>
      <div class="divider"></div>
      <div class="reader-info">
        <div class="reader-info-row">
          <div><strong>用户ID:</strong> {{ reader.user_id }}</div>
          <div><strong>信用等级:</strong> {{ reader.credit_level }}</div>
        </div>
        <div class="reader-info-row">
          <div>
            <strong>余额:</strong> ¥{{ parseFloat(reader.balance.toFixed(2)) }}
          </div>
        </div>
        <div class="reader-info-row">
          <div><strong>地址:</strong> {{ reader.address }}</div>
        </div>
      </div>
      <div class="divider"></div>
      <div class="remaining-balance">
        <strong>剩余余额:</strong> ¥{{
          parseFloat((reader.balance - book.price).toFixed(2))
        }}
      </div>
      <div class="modal-actions">
        <button @click="$emit('cancel')">取消</button>
        <button @click="confirmPurchase">确认购买</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import { useStore } from 'vuex';
import { Book, Reader, Order } from '@/store/modules/types'; // 导入 Book, Reader, Order 接口

const props = defineProps<{
  visible: boolean;
  book: Book;
  reader: Reader;
}>();

const emit = defineEmits(['cancel', 'update-reader']);

const store = useStore();

const confirmPurchase = () => {
  if (props.reader.balance >= props.book.price) {
    const updatedReader = { ...props.reader, balance: props.reader.balance - props.book.price };
    emit('update-reader', updatedReader);

    const order: Order = {
      order_id: Date.now(),
      reader_id: props.reader.reader_id,
      book_id: props.book.book_id,
      quantity: 1,
      price: props.book.price,
      order_date: new Date().toISOString(),
      description: `Order for book ${props.book.title}`,
      shipping_address: props.reader.address,
      status: 'pending',
    };

    store.dispatch('order/addOrder', order);

    emit('cancel');
    alert('下单成功！');
  } else {
    alert('该充钱了兄弟XD');
  }
};
</script>


<style scoped>
.modal {
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
  background: white;
  padding: 20px;
  width: 400px;
  border-radius: 8px;
}

.modal-header {
  font-size: 24px;
  margin-bottom: 10px;
}

.book-info div,
.reader-info-row div {
  margin-bottom: 5px;
}

.reader-info-row {
  display: flex;
  justify-content: space-between;
}

.divider {
  height: 1px;
  background-color: #ddd;
  margin: 20px 0;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>
