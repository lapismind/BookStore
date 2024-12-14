<template>
  <div v-if="visible" class="modal">
    <div class="modal-content">
      <h2 class="modal-header">订单详情</h2>
      <div class="book-info">
        <div>
          <strong>书名:</strong>
          <span class="book-title">{{ book.title }}</span>
        </div>
        <div><strong>出版日期:</strong> {{ book.publication_date }}</div>
        <div><strong>作者:</strong> {{ book.author }}</div>
        <div><strong>出版商:</strong> {{ book.publisher }}</div>
        <div><strong>简介:</strong> 暂无</div>
        <div><strong>价格:</strong> ¥{{ book.price }}</div>
      </div>
      <div class="divider"></div>
      <div class="reader-info">
        <div class="reader-info-row">
          <div><strong>用户ID:</strong> {{ reader.user_id }}</div>
          <div><strong>信用等级:</strong> {{ reader.credit_level }}</div>
        </div>
        <div class="reader-info-row">
          <div>
            <strong>余额:</strong> ¥{{ parseFloat(reader.balance.toFixed(2)) }}
          </div>
        </div>
        <div class="reader-info-row">
          <div><strong>地址:</strong> {{ reader.address }}</div>
        </div>
      </div>
      <div class="divider"></div>
      <div class="remaining-balance">
        <strong>剩余余额:</strong> ¥{{
          parseFloat((reader.balance - book.price).toFixed(2))
        }}
      </div>
      <div class="modal-actions">
        <button @click="$emit('cancel')">取消</button>
        <button @click="confirmPurchase">确认购买</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    visible: Boolean,
    book: Object,
    reader: Object,
  },
  methods: {
    confirmPurchase() {
      // 检查余额是否足够
      if (this.reader.balance >= this.book.price) {
        // 如果余额足够，执行购买逻辑
        this.reader.balance -= this.book.price; // 更新余额
        this.$emit("update-reader", this.reader); // 触发事件，传递更新后的 reader 对象
        this.$emit("cancel"); // 关闭弹窗
        alert("购买成功！");
      } else {
        // 如果余额不足，给出提示
        alert("该充钱了兄弟XD");
      }
    },
  },
};
</script>

<style scoped>
.modal {
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
  background: white;
  padding: 20px;
  width: 400px;
  border-radius: 8px;
}

.modal-header {
  font-size: 24px; /* 加大标题 */
  margin-bottom: 10px;
}

.book-info div,
.reader-info-row div {
  margin-bottom: 5px;
}

.reader-info-row {
  display: flex;
  justify-content: space-between;
}

.divider {
  height: 1px; /* 分割线高度 */
  background-color: #ddd; /* 分割线颜色 */
  margin: 20px 0; /* 分割线与上下内容的间距 */
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>
