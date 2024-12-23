<template>
  <div v-if="visible" class="shortage-record">
    <div class="modal-content">
      <h2>缺书登记表</h2>

      <!-- 登记表单 -->
      <form @submit.prevent="addShortageRecord" class="shortage-form">
        <div class="form-row">
          <div class="form-group">
            <label class="inline-label" for="bookId">书籍ID:</label>
            <input type="text" id="bookId" v-model="newShortageRecord.book_id" required />
          </div>
          <div class="form-group">
            <label class="inline-label" for="seriesId">系列ID:</label>
            <input type="number" id="seriesId" v-model.number="newShortageRecord.series_id" required />
          </div>
          <div class="form-group">
            <label class="inline-label" for="publisher">出版社:</label>
            <input type="text" id="publisher" v-model="newShortageRecord.publisher" required />
          </div>
          <div class="form-group">
            <label class="inline-label" for="supplier">供应商:</label>
            <input type="text" id="supplier" v-model="newShortageRecord.supplier" required />
          </div>
          <div class="form-group">
            <label class="inline-label" for="quantity">缺货数目:</label>
            <input type="number" id="quantity" v-model.number="newShortageRecord.quantity" required />
          </div>
          <button type="submit" class="action-button">登记</button>
        </div>
      </form>

      <!-- 表格 -->
      <table>
        <thead>
        <tr>
          <th>缺书登记ID</th>
          <th>书ID</th>
          <th>系列ID</th>
          <th>出版社</th>
          <th>供应商</th>
          <th>数目</th>
          <th>登记日期</th>
          <th>处理状态</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="record in paginatedRecords" :key="record.shortage_id">
          <td>{{ record.shortage_id }}</td>
          <td>{{ record.book_id }}</td>
          <td>{{ record.series_id }}</td>
          <td>{{ record.publisher }}</td>
          <td>{{ record.supplier }}</td>
          <td>{{ record.quantity }}</td>
          <td>{{ record.record_date }}</td>
          <td>{{ record.processed ? '已处理' : '未处理' }}</td>
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
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import type { BookShortage } from '@/store/modules/types';

const props = defineProps({
  visible: Boolean,
});

const emit = defineEmits(['close']);

const store = useStore();

const newShortageRecord = ref<BookShortage>({
  shortage_id: 0,
  book_id: '',
  series_id: 0,
  publisher: '',
  supplier: '',
  quantity: 0,
  record_date: new Date().toISOString(),
  processed: false,
});

const shortageRecords = computed(() => store.getters['record/shortageRecords'] || []);

onMounted(async () => {
  await store.dispatch('record/fetchShortageRecords');
});

const addShortageRecord = async () => {
  try {
    const newRecord = { ...newShortageRecord.value };
    newRecord.shortage_id = Math.max(...shortageRecords.value.map((r: BookShortage) => r.shortage_id), 0) + 1;
    newRecord.record_date = new Date().toISOString();
    await store.dispatch('record/addShortageRecord', newRecord);
    newShortageRecord.value = {
      shortage_id: 0,
      book_id: '',
      series_id: 0,
      publisher: '',
      supplier: '',
      quantity: 0,
      record_date: new Date().toISOString(),
      processed: false,
    };
  } catch (error) {
    console.error('Failed to add shortage record:', error);
  }
};

const handleClose = () => {
  emit('close');
};

// Pagination logic
const currentPage = ref(1);
const recordsPerPage = 6;

const paginatedRecords = computed(() => {
  const start = (currentPage.value - 1) * recordsPerPage;
  const end = start + recordsPerPage;
  return shortageRecords.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(shortageRecords.value.length / recordsPerPage);
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
.shortage-record {
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

.form-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.inline-label {
  margin-right: 10px;
  white-space: nowrap;
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