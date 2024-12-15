<template>
  <div>
    <!-- Dropdown component with Reader component inside -->
    <Dropdown triggerText="User Icon">
      <ReaderInfo :reader="reader" />
    </Dropdown>
    <!-- 使用 v-for 渲染多本书籍 -->
    <BookDetails
      v-for="book in books"
      :key="book.book_id"
      :book="book"
      :reader="reader"
      @update-reader="updateReader"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex';
import BookDetails from "@/components/BookDetails.vue";
import ReaderInfo from "@/components/ReaderInfo.vue";
import Dropdown from "@/components/Dropdown.vue";

export default {
  components: {
    BookDetails,
    ReaderInfo,
    Dropdown,
  },
  computed: {
    ...mapState('book', ['books']),
    ...mapState('user', ['reader']),
  },
  methods: {
    updateReader(updatedReader) {
      this.$store.commit('user/SET_READER', updatedReader);
    },
  },
};
</script>

<style scoped>
/* 页面样式，可以根据需求添加 */
</style>
