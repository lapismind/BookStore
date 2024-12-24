<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <span class="close" @click="$emit('close')">&times;</span>
      <h2>搜索书目信息</h2>
      <form @submit.prevent="performSearch">
        <div>
          <label for="id">ID:</label>
          <input type="text" v-model="searchQuery.id" />
        </div>
        <div>
          <label for="title">Title:</label>
          <input type="text" v-model="searchQuery.title" />
        </div>
        <div>
          <label for="publisher">Publisher:</label>
          <input type="text" v-model="searchQuery.publisher" />
        </div>
        <div>
          <label for="keywords">Keywords:</label>
          <input type="text" v-model="searchQuery.keywords" />
        </div>
        <div>
          <label for="author">Author:</label>
          <input type="text" v-model="searchQuery.author" />
        </div>
        <button type="submit" class="action-button">搜索</button>
      </form>
      <div v-if="books.length > 0">
        <h3>搜索结果</h3>
        <ul>
          <li v-for="book in books" :key="book.book_id">
            {{ book.title }} by {{ book.author }}
          </li>
        </ul>
      </div>
      <div v-else>
        <p>未找到书目。</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import type { Book } from '@/store/modules/types';

const props = defineProps<{ visible: boolean }>();
const store = useStore();

const searchQuery = ref({
  id: '',
  title: '',
  publisher: '',
  keywords: '',
  author: '',
});

const books = computed<Book[]>(() => {
  return store.getters['book/searchBooks'](searchQuery.value);
});

const performSearch = () => {
  // Trigger the computed property to update
  books.value;
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