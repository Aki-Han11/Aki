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
    <el-empty v-else description="No orders yet" />
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
h1 { margin-bottom: 28px; font-size: 28px; font-weight: 700; color: #1a1815; letter-spacing: -0.4px; }
.order-list { display: flex; flex-direction: column; gap: 12px; }
.order-item {
  display: flex; align-items: center; justify-content: space-between;
  background: #fefdfc; padding: 22px 24px; border-radius: 16px; cursor: pointer;
  border: 1px solid #f1ede7;
  box-shadow: 0 1px 3px rgba(0,0,0,0.018), 0 1px 2px rgba(0,0,0,0.022);
  transition: all 0.25s ease;
}
.order-item:hover { box-shadow: 0 10px 24px rgba(0,0,0,0.05); border-color: #e3dbd1; }
.order-info h3 { font-size: 16px; font-weight: 600; color: #1a1815; }
.order-info p { color: #a0988c; font-size: 13px; margin-top: 2px; }
.order-meta { display: flex; align-items: center; gap: 16px; }
.order-price { font-size: 18px; color: #1a1815; font-weight: 600; }
</style>
