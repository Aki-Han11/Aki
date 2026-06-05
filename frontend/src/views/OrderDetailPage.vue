<template>
  <div class="order-detail-page">
    <el-button text @click="$router.push('/orders')"><el-icon><ArrowLeft /></el-icon> Back to Orders</el-button>
    <h1>Order #{{ order.id }}</h1>
    <div v-if="loading"><el-skeleton :rows="6" animated /></div>
    <template v-else-if="order.id">
      <el-card class="order-card">
        <div class="order-header">
          <div><strong>Status:</strong> <el-tag :type="statusType(order.status)">{{ order.status }}</el-tag></div>
          <div><strong>Date:</strong> {{ new Date(order.created_at).toLocaleString() }}</div>
          <div><strong>Total:</strong> <span class="price">${{ order.total_price }}</span></div>
        </div>
        <el-divider />
        <h3>Items</h3>
        <div class="item-list">
          <div v-for="item in order.items" :key="item.id" class="item-row">
            <img v-if="item.book" :src="item.book.cover_url" :alt="item.book.title" class="item-cover" @error="e => e.target.src='https://picsum.photos/seed/default/200/300'" />
            <div class="item-info">
              <router-link :to="item.book ? `/books/${item.book.id}` : '#'"><h4>{{ item.book?.title || 'N/A' }}</h4></router-link>
              <p>{{ item.book?.author }}</p>
            </div>
            <div class="item-price">${{ item.price }}</div>
          </div>
        </div>
        <div class="order-actions" v-if="order.status === 'pending'">
          <el-button type="success" @click="handlePay" :loading="paying">Pay Now</el-button>
          <el-button type="danger" plain @click="handleCancel" :loading="cancelling">Cancel Order</el-button>
        </div>
      </el-card>
    </template>
    <el-empty v-else description="Order not found" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getOrderDetail, payOrder, cancelOrder } from '../api/endpoints'

const route = useRoute()
const order = ref({})
const loading = ref(true)
const paying = ref(false)
const cancelling = ref(false)

function statusType(s) {
  const m = { pending: 'warning', paid: 'success', cancelled: 'info', completed: 'success' }
  return m[s] || 'info'
}

async function fetchOrder() {
  loading.value = true
  try {
    const res = await getOrderDetail(route.params.id)
    order.value = res.data
  } catch (e) { order.value = {} }
  loading.value = false
}

async function handlePay() {
  paying.value = true
  try {
    await payOrder(order.value.id)
    ElMessage.success('Payment successful')
    fetchOrder()
  } catch (e) { ElMessage.error('Payment failed') }
  paying.value = false
}

async function handleCancel() {
  cancelling.value = true
  try {
    await cancelOrder(order.value.id)
    ElMessage.success('Order cancelled')
    fetchOrder()
  } catch (e) { ElMessage.error('Failed to cancel') }
  cancelling.value = false
}

onMounted(fetchOrder)
</script>

<style scoped>
h1 { margin: 16px 0 24px; }
.order-card { max-width: 800px; }
.order-header { display: flex; gap: 24px; flex-wrap: wrap; }
.price { color: #f56c6c; font-weight: 700; font-size: 20px; }
.item-list { display: flex; flex-direction: column; gap: 12px; }
.item-row { display: flex; align-items: center; gap: 16px; padding: 12px; background: #f5f7fa; border-radius: 8px; }
.item-cover { width: 50px; height: 70px; object-fit: cover; border-radius: 4px; }
.item-info { flex: 1; }
.item-info h4 { font-size: 15px; }
.item-info p { color: #999; font-size: 13px; }
.item-price { font-weight: 600; }
.order-actions { margin-top: 20px; display: flex; gap: 12px; }
</style>
