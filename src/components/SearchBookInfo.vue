<script setup lang="ts">
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { Book } from '@/store/modules/types';

const store = useStore();

const searchQuery = ref({
  id: '',
  title: '',
  publisher: '',
  keywords: '',
  author: '',
});

const searchBooks = computed<Book[]>(() => {
  return store.getters['book/searchBooks'](searchQuery.value);
});

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};
</script>

<template>
  <div>
    <button @click="openModal" class="action-button">书目查询</button>
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-button" @click="closeModal">X</button>
        <form @submit.prevent>
          <div class="form-group">
            <label for="id">ID:</label>
            <input type="text" id="id" v-model="searchQuery.id" />
          </div>
          <div class="form-group">
            <label for="title">Title:</label>
            <input type="text" id="title" v-model="searchQuery.title" />
          </div>
          <div class="form-group">
            <label for="publisher">Publisher:</label>
            <input type="text" id="publisher" v-model="searchQuery.publisher" />
          </div>
          <div class="form-group">
            <label for="keywords">Keywords:</label>
            <input type="text" id="keywords" v-model="searchQuery.keywords" />
          </div>
          <div class="form-group">
            <label for="author">Author:</label>
            <input type="text" id="author" v-model="searchQuery.author" />
          </div>
        </form>
        <div v-if="searchBooks.length > 0">
          <h2>Search Results:</h2>
          <ul>
            <li v-for="book in searchBooks" :key="book.book_id">{{ book.title }} by {{ book.author }}</li>
          </ul>
        </div>
        <div v-else>
          <p>No books found.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
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
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 500px;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.form-group label {
  margin-right: 10px;
}

.form-group input {
  flex: 1;
  padding: 8px;
  box-sizing: border-box;
}
</style>