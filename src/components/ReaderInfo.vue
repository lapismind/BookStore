<!-- ReaderInfo.vue -->
<template>
  <div class="reader">
    <div class="reader-header">
      <img src="path-to-your-image.png" alt="我是头像" class="reader-avatar" />
    </div>
    <p>UID：{{ reader.reader_id }}</p>
    <p>{{ reader.user_id }}</p>
    <p>我的余额：{{ reader.balance }}</p>
    <p>信用等级：{{ reader.credit_level }}</p>

    <div class="options">
      <a href="javascript:void(0);" class="option" @click="handleProfile">
        个人中心
      </a>
      <a href="javascript:void(0);" class="option" @click="handleOrders">
        我的订单
      </a>
      <a href="javascript:void(0);" class="option" @click="handleRecharge">
        余额充值
      </a>
      <a href="javascript:void(0);" class="option" @click="handleLogout">
        退出登录
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "ReaderInfo",
  props: {
    reader: {
      type: Object,
      required: true,
    },
  },
  methods: {
    handleProfile() {
      // 处理个人中心逻辑
    },
    handleOrders() {
      // 处理我的订单逻辑
    },
    handleRecharge() {
      // 处理余额充值逻辑
    },
    handleLogout() {
      // 处理退出登录逻辑
    },
  },
};
</script>

<style scoped>
.reader {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  color: #333;
}

.reader-header img {
  width: 100px; /* 根据需要调整图片大小 */
  height: 100px;
  border-radius: 50%; /* 圆形图片 */
  object-fit: cover; /* 确保图片内容适应圆形 */
}

.reader p {
  font-size: 16px;
  line-height: 1.5;
}

.options {
  margin-top: 20px;
}

.option {
  display: block;
  margin-bottom: 10px;
  color: #007bff;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.3s ease;
}

.option:hover {
  color: #0056b3;
}
</style>
