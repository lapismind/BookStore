<template>
  <div class="dropdown">
    <button @click="toggleDropdown" class="dropdown-button">
      <img src="@/assets/user.svg" alt="用户图标" class="dropdown-avatar" />
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
  top: 10px;
  right: 10px;
}

.dropdown-button {
  padding: 0px;
  background-color: #fff;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  outline: none;
}

.dropdown-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
}

.dropdown-content {
  position: absolute;
  right: 0;
  top: 100%;
  background-color: #f9f9f9;
  min-width: 180px;
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 15px 20px;
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