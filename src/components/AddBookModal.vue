<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <span class="close" @click="$emit('close')">&times;</span>
      <h2>新书入库</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="book_id">ISBN:</label>
          <input type="text" v-model="newBook.book_id" required />
        </div>
        <div>
          <label for="series_id">丛书号:</label>
          <input type="number" v-model="newBook.series_id" required />
        </div>
        <div>
          <label for="title">书名:</label>
          <input type="text" v-model="newBook.title" required />
        </div>
        <div>
          <label for="author">作者:</label>
          <input type="text" v-model="authorInput" required />
        </div>
        <div>
          <label for="publication_date">出版日期:</label>
          <input type="date" v-model="newBook.publication_date" required />
        </div>
        <div>
          <label for="price">价格:</label>
          <input type="number" v-model="newBook.price" required />
        </div>
        <div>
          <label for="publisher">出版社:</label>
          <input type="text" v-model="newBook.publisher" required />
        </div>
        <div>
          <label for="keywords">关键字:</label>
          <input type="text" v-model="keywordsInput" required />
        </div>
        <div>
          <label for="total_stock">库存数量:</label>
          <input type="number" v-model="newBook.total_stock" required />
        </div>
        <div>
          <label for="supplier">供应商:</label>
          <input type="text" v-model="supplierInput" required />
        </div>
        <button type="submit">添加书籍</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { Book } from '@/store/modules/types';
import { reactive, ref, watch, defineComponent } from 'vue';

export default defineComponent({
  name: 'AddBookModal',
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
  },
  setup(props: { visible: boolean }, { emit }) {
    const newBook = reactive<Book>({
      book_id: '',
      series_id: 0,
      title: '',
      author: [],
      publication_date: '',
      price: 0,
      publisher: '',
      keywords: [],
      total_stock: 0,
      supplier: [],
    });

    const authorInput = ref('');
    const keywordsInput = ref('');
    const supplierInput = ref('');

    watch(authorInput, (newVal) => {
      newBook.author = newVal.split(',').map((item) => item.trim());
    });

    watch(keywordsInput, (newVal) => {
      newBook.keywords = newVal.split(',').map((item) => item.trim());
    });

    watch(supplierInput, (newVal) => {
      newBook.supplier = newVal.split(',').map((item) => item.trim());
    });

    const submitForm = () => {
      emit('add-book', { ...newBook });
      resetForm();
      emit('close');
    };

    const resetForm = () => {
      newBook.book_id = '';
      newBook.series_id = 0;
      newBook.title = '';
      newBook.author = [];
      newBook.publication_date = '';
      newBook.price = 0;
      newBook.publisher = '';
      newBook.keywords = [];
      newBook.total_stock = 0;
      newBook.supplier = [];
      authorInput.value = '';
      keywordsInput.value = '';
      supplierInput.value = '';
    };

    return {
      newBook,
      submitForm,
      authorInput,
      keywordsInput,
      supplierInput,
    };
  },
});

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
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
}
</style>
