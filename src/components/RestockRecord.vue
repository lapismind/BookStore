<template>
  <div v-if="visible" class="restock-record">
    <div class="modal-content">
      <h2>采购记录表</h2>

      <!-- 登记表单 -->
      <form @submit.prevent="addRestockRecords" class="restock-form">
        <div class="form-row">
          <div class="form-group">
            <label class="inline-label" for="bookId">书籍ID:</label>
            <input type="text" id="bookId" v-model.number="bookId" required />
          </div>
          <div class="form-group">
            <label class="inline-label" for="quantity">采购数量:</label>
            <input type="number" id="quantity" v-model.number="quantity" required />
          </div>
          <div class="form-group book-title-group">
            <label class="inline-label" for="bookTitle">书籍标题:</label>
            <input type="text" id="bookTitle" :value="bookTitle" readonly />
          </div>
          <button type="submit" class="action-button" >登记</button>
        </div>
      </form>

      <!-- 查询表单 -->
      <form @submit.prevent="searchRecord" class="search-form">
        <div class="form-row">
          <div class="form-group">
            <label class="inline-label" for="searchId">采购ID:</label>
            <input type="text" id="searchId" v-model.number="searchId" required />
          </div>
          <button type="submit" class="action-button">查询</button>
        </div>
      </form>

      <!-- 表格 -->
      <table>
        <thead>
        <tr>
          <th>采购ID</th>
          <th>书ID</th>
          <th>库存ID</th>
          <th>采购日期</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="record in paginatedRecords" :key="record.restock_id">
          <td>{{ record.restock_id }}</td>
          <td>{{ record.book_id }}</td>
          <td>{{ record.inventory_id }}</td>
          <td>{{ record.restock_date }}</td>
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

    <!-- 查询结果弹窗 -->
    <div v-if="showSearchModal" class="modal-overlay">
      <div class="modal-content">
        <h3>查询结果</h3>
        <div v-if="searchedRecord">
          <p>采购ID: {{ searchedRecord.restock_id }}</p>
          <p>书ID: {{ searchedRecord.book_id }}</p>
          <p>库存ID: {{ searchedRecord.inventory_id }}</p>
          <p>采购日期: {{ searchedRecord.restock_date }}</p>
        </div>
        <div v-else>
          <p>无对应结果</p>
        </div>
        <button @click="closeSearchModal" class="action-button">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import type { Restock } from '@/store/modules/types';

const props = defineProps({
  visible: Boolean,
});

const emit = defineEmits(['close']);

const store = useStore();

const bookId = ref<number>(0);
const quantity = ref<number>(0);
const searchId = ref<number | null>(null);
const searchedRecord = ref<Restock | null>(null);
const showSearchModal = ref(false);

const restockRecords = computed(() => store.getters['record/restockRecords'] || []);

const bookTitle = computed(() => {
  const book = store.getters['book/getBookById'](bookId.value);
  return book ? book.title : '未知书籍';
});

onMounted(async () => {
  await store.dispatch('record/fetchRestockRecords');
});

const addRestockRecords = async () => {
  try {
    for (let i = 0; i < quantity.value; i++) {
      const newRecord: Restock = {
        restock_id: Math.max(...restockRecords.value.map((r: Restock) => r.restock_id), 0) + 1,
        book_id: bookId.value,
        inventory_id: Math.max(...restockRecords.value.map((r: Restock) => r.inventory_id), 0) + 1,
        restock_date: new Date(),
      };
      await store.dispatch('record/addRestockRecord', newRecord.book_id);
      store.commit('record/ADD_RESTOCK_RECORD', newRecord);
    }
    bookId.value = 0;
    quantity.value = 0;
  } catch (error) {
    console.error('Failed to add restock records:', error);
  }
};

const searchRecord = () => {
  searchedRecord.value = store.getters['record/getRestockById'](searchId.value);
  showSearchModal.value = true;
};

const closeSearchModal = () => {
  showSearchModal.value = false;
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
  return restockRecords.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(restockRecords.value.length / recordsPerPage);
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
.restock-record {
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

#bookId, #quantity {
  width: 60px; /* Adjusted width */
}

#bookTitle {
  flex: 1; /* Take remaining space */
}

.form-group.book-title-group {
  flex: 1; /* Take half the length */
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

.action-button {
  margin-top: 20px;
}
</style>