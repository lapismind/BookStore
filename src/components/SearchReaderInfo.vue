<template>
  <div>
    <button @click="openModal" class="action-button">用户查询</button>
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-button" @click="closeModal">X</button>
        <form @submit.prevent>
          <div class="form-group">
            <label for="readerId">Reader ID:</label>
            <input type="text" id="readerId" v-model="searchQuery.readerId" />
          </div>
          <div class="form-group">
            <label for="userId">User ID:</label>
            <input type="text" id="userId" v-model="searchQuery.userId" />
          </div>
        </form>
        <div v-if="searchReaders.length > 0">
          <h2>User Information:</h2>
          <ul>
            <li v-for="reader in searchReaders" :key="reader.reader_id">
              <p>Reader ID: {{ reader.reader_id }}</p>
              <p>Name: {{ reader.user_id }}</p>
              <p>Address: {{ reader.address }}</p>
              <p>Balance: {{ reader.balance }}</p>
              <p>Credit Level: {{ reader.credit_level }}</p>
              <SearchOrdersInfo :readerId="reader.reader_id" />
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No users found.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import SearchOrdersInfo from '@/components/SearchOrdersInfo.vue';

const store = useStore();

const searchQuery = ref({
  readerId: '',
  userId: '',
});

const searchReaders = computed(() => {
  return store.getters['user/searchReaders'](searchQuery.value);
});

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};
</script>

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
  position: relative;
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