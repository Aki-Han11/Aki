<template>
  <div class="orders-page">
    <h1>My Orders</h1>
    <div v-if="loading"><el-skeleton :rows="5" animated /></div>
    <template v-else-if="orders.length">
      <div class="order-list">
        <div v-for="order in orders" :key="order.id" class="order-item" @click="$router.push(`/orders/${order.id}`)">
          <div class="order-info">
            <h3>Order #{{ order.id }}</h3>
            <p>{{ new Date(order.created_at).toLocaleDateString() }}</p>
          </div>
          <div class="order-meta">
            <el-tag :type="statusType(order.status)">{{ order.status }}</el-tag>
            <span class="order-price">${{ order.total_price }}</span>
          </div>
        </div>
      </div>
    </template>
    <el-empty v-else description="No orders yet">
      <el-button type="primary" @click="$router.push('/books')">Browse Books</el-button>
    </el-empty>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getOrders } from '../api/endpoints'

const orders = ref([])
const loading = ref(true)

function statusType(status) {
  const map = { pending: 'warning', paid: 'success', cancelled: 'info', completed: 'success' }
  return map[status] || 'info'
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await getOrders()
    orders.value = res.data.results || res.data
  } catch (e) {
    orders.value = []
  }
  loading.value = false
})
</script>

<style scoped>
.orders-page { max-width: 900px; margin: 0 auto; padding: 0 32px; }
h1 { margin-bottom: 36px; font-size: 28px; font-weight: 700; color: #1a1815; letter-spacing: -0.5px; }
.order-list { display: flex; flex-direction: column; }
.order-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 22px 0; cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.2s ease;
}
.order-item:hover { background: #ffffff; }
.order-info h3 { font-size: 16px; font-weight: 600; color: #1a1815; }
.order-info p { color: #a0988c; font-size: 13px; margin-top: 2px; }
.order-meta { display: flex; align-items: center; gap: 16px; }
.order-price { font-size: 18px; color: #1a1815; font-weight: 600; }

@media (max-width: 640px) {
  .orders-page { padding: 0 16px; }
  .order-item { flex-wrap: wrap; gap: 8px; }
  .order-price { font-size: 16px; }
}
</style>
