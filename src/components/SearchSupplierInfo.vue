<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <span class="close" @click="$emit('close')">&times;</span>
      <h2>搜索供应商信息</h2>
      <form @submit.prevent="searchSupplier">
        <div>
          <label for="supplierId">供应商ID:</label>
          <input type="text" v-model="supplierId" required />
        </div>
        <button type="submit" class="action-button">搜索</button>
      </form>
      <div v-if="supplier">
        <h3>供应商信息</h3>
        <p>名称: {{ supplier.name }}</p>
        <p>书籍列表:</p>
        <ul>
          <li v-for="book in supplier.book_list" :key="book.book_id">
            {{ book.book_id }} - {{ book.series_id }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useStore } from 'vuex';
import type { Supplier } from '@/store/modules/types';

const props = defineProps<{ visible: boolean }>();
const store = useStore();

const supplierId = ref('');
const supplier = ref<Supplier | null>(null);

const searchSupplier = async () => {
  const suppliers = store.getters['supplier/suppliers'];
  supplier.value = suppliers.find((s: Supplier) => s.supplier_id === parseInt(supplierId.value));
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