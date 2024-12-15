<template>
  <div v-if="visible" class="shortage-record">
    <div class="modal-content">
      <h2>缺书登记表</h2>

      <!-- 表单 -->
      <form @submit.prevent="addShortageRecord" class="shortage-form">
        <div class="form-row">
          <div class="form-group">
            <label class="inline-label" for="bookId">书籍ID:</label>
            <input type="text" id="bookId" v-model="newShortageRecord.book_id" required />
          </div>
          <div class="form-group">
            <label class="inline-label" for="quantity">缺货数目:</label>
            <input type="number" id="quantity" v-model="newShortageRecord.quantity" required />
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
          <th>供书商</th>
          <th>数目</th>
          <th>登记日期</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="record in shortageRecords" :key="record.shortage_id">
          <td>{{ record.shortage_id }}</td>
          <td>{{ record.book_id }}</td>
          <td>{{ record.supplier }}</td>
          <td>{{ record.quantity }}</td>
          <td>{{ record.record_date }}</td>
        </tr>
        </tbody>
      </table>

      <button @click="$emit('close')" class="action-button">关闭</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import type { BookShortage, ShortageRecordForm } from '@/store/modules/record';

const props = defineProps({
  visible: Boolean,
});

const emit = defineEmits(['close']);

const store = useStore();

// 定义缺书记录列表
const shortageRecords = ref<BookShortage[]>([]);

// 获取缺书记录
const fetchShortageRecords = async () => {
  // 假设 Vuex store 中有一个 action 来获取缺书记录
  const records = await store.dispatch('book/fetchShortageRecords');
  shortageRecords.value = records;
};

// 添加新的缺书记录
const newShortageRecord = ref<ShortageRecordForm>({
  book_id: 0,
  supplier: '',
  quantity: 0,
});

const addShortageRecord = async () => {
  // 假设 Vuex store 中有一个 action 来添加缺书记录
  await store.dispatch('book/addShortageRecord', newShortageRecord.value);
  // 重新获取缺书记录
  fetchShortageRecords();
  // 重置表单
  newShortageRecord.value = {
    book_id: 0,
    supplier: '',
    quantity: 0,
  };
};

onMounted(() => {
  if (props.visible) {
    fetchShortageRecords();
  }
});
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
  width: 600px; /* 增加宽度以提供更多空间 */
}

.form-row {
  display: flex;
  align-items: center;
  justify-content: space-between; /* 使输入框和按钮之间的空间均匀分布 */
  margin-bottom: 20px;
}

.form-group {
  flex: 1; /* 使表单组占据相同的空间 */
  display: flex;
  align-items: center; /* 垂直居中对齐 */
}

.inline-label {
  margin-right: 10px; /* 标签和输入框之间的间距 */
  white-space: nowrap; /* 防止标签换行 */
}

.form-group input {
  width: 100px; /* 增加输入框宽度 */
  padding: 4px;
  border: 1px solid #ccc;
  border-radius: 4px;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  margin-bottom: 20px; /* 增加与关闭按钮的间距 */
}

table th, table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

table th {
  background-color: #f2f2f2;
}
</style>