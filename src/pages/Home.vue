<template>
  <div class="container">
    <h1 class="title">网上书店管理系统</h1>
    <nav class="nav-bar">
      <router-link to="/book-browser" class="nav-link">
        <img src="@/assets/userLogin.svg" alt="User Login" class="icon" />
        <span>书虫</span>
      </router-link>
      <router-link to="/book-manage" class="nav-link">
        <img src="@/assets/adminLogin.svg" alt="Admin Login" class="icon" />
        <span>店长</span>
      </router-link>
    </nav>
  </div>
</template>

<script>
export default {
  // 组件逻辑
};
</script>

<style scoped>
.container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 255, 255, 0.5);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.title {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 20px;
}

.nav-bar {
  display: flex;
  justify-content: center;
  gap: 100px;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.nav-link {
  text-decoration: none;
  color: #007bff;
  font-weight: 500;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s, color 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #0056b3;
  transform: scale(1.1);
}

.icon {
  width: 100px;
  height: 100px;
  margin-bottom: 8px;
}
</style>