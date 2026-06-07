<template>
  <div class="cart-page">
    <h1>Shopping Cart</h1>
    <div v-if="loading"><el-skeleton :rows="5" animated /></div>
    <template v-else-if="cartItems.length">
      <div class="cart-list">
        <div v-for="item in cartItems" :key="item.id" class="cart-item">
          <img :src="item.book.cover_url" :alt="item.book.title" class="cart-cover" @error="e => e.target.src='https://picsum.photos/seed/default/200/300'" />
          <div class="cart-info">
            <router-link :to="`/books/${item.book.id}`"><h3>{{ item.book.title }}</h3></router-link>
            <p>{{ item.book.author }}</p>
          </div>
          <div class="cart-price">${{ item.book.price }}</div>
          <div class="cart-qty">Qty: {{ item.quantity }}</div>
          <el-button type="danger" plain size="small" @click="handleRemove(item)">Remove</el-button>
        </div>
      </div>
      <div class="cart-footer">
        <div class="cart-total">Total: <strong>${{ totalPrice }}</strong></div>
        <el-button type="primary" size="large" @click="handleCheckout" :loading="checkingOut">Checkout</el-button>
      </div>
    </template>
    <el-empty v-else description="Your cart is empty">
      <el-button type="primary" @click="$router.push('/books')">Browse Books</el-button>
    </el-empty>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCart, removeFromCart, checkout } from '../api/endpoints'
import { useCartStore } from '../store/cart'

const router = useRouter()
const cartStore = useCartStore()

const cartItems = ref([])
const loading = ref(true)
const checkingOut = ref(false)

const totalPrice = computed(() =>
  cartItems.value.reduce((sum, item) => sum + parseFloat(item.book.price) * item.quantity, 0).toFixed(2)
)

async function fetchCart() {
  loading.value = true
  try {
    const res = await getCart()
    cartItems.value = res.data.results || res.data
  } catch (e) {
    cartItems.value = []
  }
  loading.value = false
}

async function handleRemove(item) {
  try {
    await removeFromCart(item.id)
    cartItems.value = cartItems.value.filter(i => i.id !== item.id)
    cartStore.fetch()
    ElMessage.success('Removed')
  } catch (e) {
    ElMessage.error('Failed')
  }
}

async function handleCheckout() {
  checkingOut.value = true
  try {
    const res = await checkout()
    ElMessage.success('Order created! Redirecting to orders...')
    cartStore.fetch()
    router.push(`/orders/${res.data.order_id}`)
  } catch (e) {
    ElMessage.error(e.response?.data?.error || 'Checkout failed')
  }
  checkingOut.value = false
}

onMounted(fetchCart)
</script>

<style scoped>
h1 { margin-bottom: 28px; font-size: 28px; font-weight: 700; color: #1a1815; letter-spacing: -0.4px; }
.cart-list { display: flex; flex-direction: column; gap: 14px; }
.cart-item {
  display: flex; align-items: center; gap: 18px;
  background: #fffdfa; padding: 18px; border-radius: 16px;
  border: 1px solid #f0ece6;
  box-shadow: 0 1px 3px rgba(0,0,0,0.018), 0 1px 2px rgba(0,0,0,0.022);
}
.cart-cover { width: 65px; height: 92px; object-fit: cover; border-radius: 8px; }
.cart-info { flex: 1; }
.cart-info h3 { font-size: 16px; font-weight: 600; color: #1a1815; }
.cart-info p { color: #a0988c; font-size: 14px; }
.cart-price { color: #1a1815; font-weight: 600; font-size: 16px; }
.cart-qty { color: #8b7e74; font-size: 14px; }
.cart-footer {
  margin-top: 24px; padding: 22px 24px; background: #fffdfa;
  border-radius: 16px; display: flex; align-items: center;
  justify-content: space-between;
  border: 1px solid #f0ece6;
  box-shadow: 0 1px 3px rgba(0,0,0,0.018);
}
.cart-total { font-size: 20px; color: #4a4038; }
.cart-total strong { color: #1a1815; }
</style>
