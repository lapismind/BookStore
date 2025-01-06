<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <span class="close" @click="$emit('close')">&times;</span>
      <h2>新增供应商</h2>
      <form @submit.prevent="addSupplier">
        <div>
          <label for="name">名称:</label>
          <input type="text" v-model="name" required />
        </div>
        <div v-for="(book, index) in books" :key="index" class="book-entry">
          <h3>书籍 {{ index + 1 }}</h3>
          <div>
            <label for="book_id">书籍ID:</label>
            <input type="text" v-model="book.book_id" required />
          </div>
          <div>
            <label for="series_id">系列ID:</label>
            <input type="number" v-model="book.series_id" required />
          </div>
        </div>
        <button type="button" @click="addBook" class="action-button"pnp>添加书籍</button>
        <button type="submit" class="action-button">提交</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useStore } from 'vuex';

const props = defineProps<{ visible: boolean }>();
const emit = defineEmits(['close']);
const store = useStore();

const name = ref('');
const books = ref([{ book_id: '', series_id: 0 }]);

const addBook = () => {
  books.value.push({ book_id: '', series_id: 0 });
};

const addSupplier = async () => {
  await store.dispatch('supplier/addSupplier', { name: name.value, book_list: books.value });
  name.value = '';
  books.value = [{ book_id: '', series_id: 0 }];
  emit('close');
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

.book-entry {
  margin-bottom: 15px;
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