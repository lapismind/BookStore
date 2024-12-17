<template>
  <div class="nav-container">
  <router-link to="/book-list" class="nav-link">
    <img src="@/assets/bookList.svg" alt="书籍列表" class="icon" />
    <span class="nav-text">书籍列表</span>
  </router-link>
  <router-link to="/book-manage" class="nav-link">
    <img src="@/assets/bookManage.svg" alt="库存管理" class="icon" />
    <span class="nav-text">库存管理</span>
  </router-link>
  <router-link to="/user-manage" class="nav-link">
    <img src="@/assets/userManage.svg" alt="用户管理" class="icon" />
    <span class="nav-text">用户管理</span>
  </router-link>
  <router-link to="/order-manage" class="nav-link">
    <img src="@/assets/orderManage.svg" alt="用户订单管理" class="icon" />
    <span class="nav-text">用户订单管理</span>
  </router-link>
  <router-link to="/supplier-manage" class="nav-link">
    <img src="@/assets/supplierManage.svg" alt="供应商管理" class="icon" />
    <span class="nav-text">供应商管理</span>
  </router-link>
  <router-link to="/search" class="nav-link">
    <img src="@/assets/search.svg" alt="搜索" class="icon" />
    <span class="nav-text">搜索</span>
  </router-link>
  <router-link to="/home" class="nav-link">
    <img src="@/assets/exit.svg" alt="退出管理页面" class="icon" />
    <span class="nav-text">退出管理页面</span>
  </router-link>
</div>
</template>

<style scoped>

</style>
<script setup lang="ts">
</script>