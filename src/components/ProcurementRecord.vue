<template>
  <div v-if="visible" class="procurement-record">
    <div class="modal-content">
      <h2>采购记录表</h2>

      <!-- 新增表单 -->
      <form @submit.prevent="addProcurementOrder" class="procurement-form">
        <div class="form-row">
          <div class="form-group">
            <label class="inline-label" for="bookId">书籍ID:</label>
            <input type="text" id="bookId" v-model="newOrder.book_id" required />
          </div>
          <div class="form-group">
            <label class="inline-label" for="seriesId">系列ID:</label>
            <input type="number" id="seriesId" v-model.number="newOrder.series_id" required />
          </div>
          <div class="form-group">
            <label class="inline-label" for="quantity">数量:</label>
            <input type="number" id="quantity" v-model.number="newOrder.quantity" required />
          </div>
          <button type="submit" class="action-button">新增</button>
        </div>
      </form>

      <!-- 表格 -->
      <table>
        <thead>
        <tr>
          <th>采购订单ID</th>
          <th>书ID</th>
          <th>系列ID</th>
          <th>数量</th>
          <th>状态</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="record in paginatedRecords" :key="record.procurement_order_id">
          <td>{{ record.procurement_order_id }}</td>
          <td>{{ record.book_id }}</td>
          <td>{{ record.series_id }}</td>
          <td>{{ record.quantity }}</td>
          <td>{{ record.status }}</td>
        </tr>
        </tbody>
      </table>

      <!-- Pagination Controls -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
        <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
      </div>

      <button @click="handleClose" class="action-button">关闭</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import type { ProcurementOrder } from '@/store/modules/types';

const props = defineProps({
  visible: Boolean,
});

const emit = defineEmits(['close']);

const store = useStore();

const newOrder = ref<ProcurementOrder>({
  procurement_order_id: 0,
  book_id: '',
  series_id: 0,
  quantity: 0,
  status: 'pending',
});

const procurementOrders = computed(() => store.getters['procure/procurementOrders'] || []);

onMounted(async () => {
  await store.dispatch('procure/fetchProcurementOrders');
});

const addProcurementOrder = async () => {
  try {
    await store.dispatch('procure/addProcurementOrder', newOrder.value);
    newOrder.value = {
      procurement_order_id: 0,
      book_id: '',
      series_id: 0,
      quantity: 0,
      status: 'pending',
    };
  } catch (error) {
    console.error('Failed to add procurement order:', error);
  }
};

const handleClose = () => {
  emit('close');
};

const currentPage = ref(1);
const recordsPerPage = 6;

const paginatedRecords = computed(() => {
  const start = (currentPage.value - 1) * recordsPerPage;
  const end = start + recordsPerPage;
  return procurementOrders.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(procurementOrders.value.length / recordsPerPage);
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};
</script>

<style scoped>
.procurement-record {
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
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 800px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  margin-bottom: 20px;
}

table th, table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

table th {
  background-color: #f2f2f2;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  margin: 0 5px;
  padding: 5px 10px;
  border: 1px solid #ccc;
  background-color: #f2f2f2;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #e0e0e0;
  cursor: not-allowed;
}

.action-button {
  margin-top: 20px;
}
</style>