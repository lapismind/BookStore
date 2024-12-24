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
        <div>
          <label for="bookList">书籍列表 (用逗号分隔书籍ID和系列ID):</label>
          <input type="text" v-model="bookList" required />
        </div>
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
const bookList = ref('');

const addSupplier = async () => {
  const books = bookList.value.split(',').map(item => {
    const [book_id, series_id] = item.trim().split('-');
    return { book_id, series_id: parseInt(series_id) };
  });
  await store.dispatch('supplier/addSupplier', { name: name.value, book_list: books });
  name.value = '';
  bookList.value = '';
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