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
h1 { margin-bottom: 24px; }
.order-list { display: flex; flex-direction: column; gap: 12px; }
.order-item {
  display: flex; align-items: center; justify-content: space-between;
  background: #fff; padding: 20px; border-radius: 8px; cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06); transition: box-shadow .2s;
}
.order-item:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
.order-info h3 { font-size: 16px; }
.order-info p { color: #999; font-size: 13px; }
.order-meta { display: flex; align-items: center; gap: 16px; }
.order-price { font-size: 18px; color: #f56c6c; font-weight: 600; }
</style>
