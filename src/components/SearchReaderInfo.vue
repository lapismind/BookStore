<template>
  <div v-if="visible" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <button class="close-button" @click="closeModal"></button>
      <form @submit.prevent>
        <div class="form-group">
          <label for="search">搜索:</label>
          <input type="text" id="search" v-model="searchQuery.searchTerm" placeholder="通过id或名称搜索" />
        </div>
      </form>
      <div v-if="searchReaders.length > 0">
        <h2>用户信息:</h2>
        <ul>
          <li v-for="reader in searchReaders" :key="reader.reader_id">
            <p>用户 ID: {{ reader.reader_id }}</p>
            <p>昵称: {{ reader.user_id }}</p>
            <p>地址: {{ reader.address }}</p>
            <p>余额: {{ reader.balance }}</p>
            <p>信用等级: {{ reader.credit_level }}</p>
            <SearchOrdersInfoByReader :readerId="reader.reader_id" />
          </li>
        </ul>
      </div>
      <div v-else>
        <p>没有找到用户</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, defineEmits } from 'vue';
import { useStore } from 'vuex';
import { Reader } from '@/store/modules/types';
import SearchOrdersInfoByReader from "@/components/SearchOrdersInfoByReader.vue";

const props = defineProps<{ visible: boolean }>();
const emit = defineEmits(['close']);

const store = useStore();

const searchQuery = ref({
  searchTerm: '',
});

const searchReaders = computed<Reader[]>(() => {
  return store.getters['user/searchReaders'](searchQuery.value.searchTerm);
});

const closeModal = () => {
  emit('close');
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