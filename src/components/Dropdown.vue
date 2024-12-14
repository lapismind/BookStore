<template>
  <div class="dropdown">
    <button @click="toggleDropdown" class="dropdown-button">
      <!-- 使用 Font Awesome 用户图标 -->
      <font-awesome-icon :icon="['fas', 'user-circle']" />
    </button>
    <transition name="fade">
      <div v-if="isOpen" class="dropdown-content">
        <slot></slot>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  props: {
    triggerText: {
      type: String,
      default: "Click me",
    },
  },
  data() {
    return {
      isOpen: false,
    };
  },
  methods: {
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },
  },
};
</script>

<style scoped>
.dropdown {
  position: fixed;
  top: 20px; /* 增加顶部距离 */
  right: 20px; /* 增加右侧距离 */
}

.dropdown-button {
  padding: 15px; /* 增加按钮内边距 */
  background-color: #fff;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  outline: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.dropdown-content {
  position: absolute;
  right: 0;
  top: 100%;
  background-color: #f9f9f9;
  min-width: 200px; /* 增加最小宽度 */
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 15px 20px; /* 增加链接内边距 */
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #f1f1f1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
