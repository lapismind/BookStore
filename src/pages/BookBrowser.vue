<template>
  <div class="book-browser" style="overflow-x: hidden;">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-logo">
        <img src="@/assets/book.svg" alt="Logo" class="logo" />
      </div>
      <div class="navbar-title">
        <h1>在线书店</h1>
      </div>
      <div class="navbar-dropdown">
        <Dropdown triggerText="User Icon">
          <ReaderInfo v-if="reader" :reader="reader" />
        </Dropdown>
      </div>
    </nav>
    <!-- 使用 v-for 渲染多本书籍 -->
    <div class="book-list">
      <BookDetails
        v-for="book in books"
        :key="book.book_id"
        :book="book"
        :reader="reader"
        @update-reader="updateReader"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useStore } from 'vuex';
import BookDetails from "@/components/BookDetails.vue";
import ReaderInfo from "@/components/ReaderInfo.vue";
import Dropdown from "@/components/Dropdown.vue";
import { Book, Reader } from '@/store/modules/types';

const store = useStore();

const reader = ref<Reader>({
  reader_id: 1,
  user_id: '',
  address: '',
  balance: 0,
  credit_level: 0,
});

const books = computed<Book[]>(() => store.state.book.books);
const readers = computed<Reader[]>(() => store.state.user.readers);

watch(readers, (newReaders) => {
  if (newReaders.length > 0) {
    reader.value = newReaders[0];
  }
}, { immediate: true });

const updateReader = (updatedReader: Reader) => {
  store.commit('user/UPDATE_READER', updatedReader);
  reader.value = updatedReader;
};

store.dispatch('user/getUserInfo', { all: true });
</script>

<style scoped>
.book-browser {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  background-color: #f8f9fa;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-logo img.logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.navbar-title h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.navbar-dropdown {
  margin-left: auto;
}

.book-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: flex-start;
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.book-list > * {
  flex: 1 1 calc(25vw - 20px);
  box-sizing: border-box;
  max-width: calc(25vw - 20px);
}

@media (max-width: 1200px) {
  .book-list > * {
    flex: 1 1 calc(33.33vw - 20px);
    max-width: calc(33.33vw - 20px);
  }
}

@media (max-width: 800px) {
  .book-list > * {
    flex: 1 1 calc(50vw - 20px);
    max-width: calc(50vw - 20px);
  }
}

@media (max-width: 600px) {
  .book-list > * {
    flex: 1 1 100vw;
    max-width: 100vw;
  }
}

@media (min-width: 960px) {
  .book-list > * {
    flex: 1 1 calc(25vw - 20px);
    max-width: calc(25vw - 20px);
  }
}
</style>