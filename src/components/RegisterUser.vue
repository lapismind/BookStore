<template>
  <div v-if="visible" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <button class="close-button" @click="closeModal">X</button>
      <h2>注册新用户</h2>
      <form @submit.prevent="registerUser">
        <input type="text" v-model="newReader.user_id" placeholder="用户昵称" required />
        <input type="text" v-model="newReader.address" placeholder="用户地址" required />
        <input type="number" v-model="newReader.balance" placeholder="用户余额" required />
        <input type="number" v-model="newReader.credit_level" placeholder="信用等级" required />
        <button type="submit">注册</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue';
import { useStore } from 'vuex';
import { Reader } from '@/store/modules/types';

const props = defineProps<{ visible: boolean }>();
const emit = defineEmits(['close']);

const store = useStore();
const newReader = ref<Reader>({
  reader_id: 0,
  user_id: '',
  address: '',
  balance: 0,
  credit_level: 0,
});

const registerUser = () => {
  store.dispatch('user/register', newReader.value).then(() => {
    resetNewReaderForm();
    closeModal();
  });
};

const resetNewReaderForm = () => {
  newReader.value = {
    reader_id: 0,
    user_id: '',
    address: '',
    balance: 0,
    credit_level: 0,
  };
};

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
  padding: 30px;
  border-radius: 10px;
  width: 90%;
  max-width: 400px;
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #aaa;
}

.close-button:hover {
  color: #000;
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
}

input {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>