<!-- Home.vue -->
<template>
  <div>
    <!-- 导航链接到 BookBrowser 和 BookManage -->
    <nav class="nav-bar">
      <router-link to="/book-browser" class="nav-link"
        >Book Browser</router-link
      >
      <router-link to="/book-manage" class="nav-link">Book Manage</router-link>
    </nav>
    <!-- 其他内容 -->
  </div>
</template>

<script>
export default {
  // 组件逻辑
};
</script>

<style scoped>
.nav-bar {
  display: flex;
  justify-content: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e7e7e7;
}

.nav-link {
  margin: 0 10px;
  padding: 10px 15px;
  text-decoration: none;
  color: #007bff;
  font-weight: 500;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: #e7f4ff;
}

.nav-link.router-link-active {
  color: #0056b3;
}
</style>
