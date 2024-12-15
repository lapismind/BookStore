<template>
 <div class="order-manage">
   <router-link to="/book-manage" class="nav-link">书籍库存管理</router-link> |
   <router-link to="/order-manage" class="nav-link">用户订单管理</router-link> |
   <router-link to="/home" class="nav-link">退出管理页面</router-link>
   <hr>
   <router-view></router-view>
 </div>
</template>

<style scoped>
.order-manage {
  padding: 20px;
}

</style>
<script setup lang="ts">
</script>