<template>
  <div class="book-detail-page">
    <div v-if="loading" class="loading-box">
      <el-skeleton :rows="10" animated />
    </div>

    <div v-else-if="book" class="detail-content">
      <div class="book-info">
        <div class="cover-section">
          <img :src="book.cover_url" :alt="book.title" class="book-cover" @error="onImgError" />
        </div>
        <div class="info-section">
          <h1>{{ book.title }}</h1>
          <p class="author">by {{ book.author }}</p>
          <el-tag v-if="book.category_name" type="info">{{ book.category_name }}</el-tag>
          <div v-if="book.tags" class="tags">
            <el-tag v-for="tag in book.tags.split(',')" :key="tag" size="small" class="tag-item">{{ tag.trim() }}</el-tag>
          </div>

          <div class="price-box">
            <span class="price">${{ book.price }}</span>
          </div>

          <div v-if="book.stats" class="stats-row">
            <span><el-icon><View /></el-icon> {{ book.stats.view_count }}</span>
            <span><el-icon><Star /></el-icon> {{ book.stats.favorite_count }}</span>
            <span><el-icon><ShoppingCart /></el-icon> {{ book.stats.purchase_count }}</span>
          </div>

          <div class="actions">
            <el-button type="primary" size="large" @click="handleBuy" :loading="buying">Buy Now</el-button>
            <el-button size="large" @click="handleAddToCart" :loading="addingCart">Add to Cart</el-button>
            <el-button size="large" @click="handleFavorite" :loading="faving" :type="isFaved ? 'warning' : 'default'">
              <el-icon><StarFilled v-if="isFaved" /><Star v-else /></el-icon>
              {{ isFaved ? 'Favorited' : 'Favorite' }}
            </el-button>
          </div>

          <div v-if="purchased" class="download-box">
            <el-button type="success" size="large" @click="handleDownload" :loading="downloading">
              <el-icon><Download /></el-icon> Download
            </el-button>
          </div>
        </div>
      </div>

      <div class="description-section">
        <h2>Description</h2>
        <p>{{ book.description || 'No description available.' }}</p>
      </div>

      <!-- Rating -->
      <div class="rating-section" v-if="auth.isLoggedIn">
        <h2>Rate This Book</h2>
        <el-rate v-model="userRating" @change="handleRate" :texts="['Poor', 'Fair', 'Good', 'Great', 'Excellent']" show-text />
      </div>
    </div>

    <div v-else class="error-box">
      <el-empty description="Book not found" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getBookDetail, addFavorite, removeFavorite, addToCart, createOrder, getBookDownload, getFavorites, rateBook } from '../api/endpoints'
import { useAuthStore } from '../store/auth'

const route = useRoute()
const auth = useAuthStore()

const book = ref(null)
const loading = ref(true)
const isFaved = ref(false)
const purchased = ref(false)
const buying = ref(false)
const addingCart = ref(false)
const faving = ref(false)
const downloading = ref(false)
const userRating = ref(0)

function onImgError(e) {
  e.target.src = 'https://picsum.photos/seed/default/200/300'
}

async function fetchBook() {
  loading.value = true
  try {
    const res = await getBookDetail(route.params.id)
    book.value = res.data
  } catch (e) {
    book.value = null
  }
  loading.value = false
}

async function checkFavorite() {
  if (!auth.isLoggedIn) return
  try {
    const res = await getFavorites()
    isFaved.value = (res.data.results || res.data).some(f => f.book.id === book.value.id)
  } catch (e) {}
}

async function checkPurchased() {
  if (!auth.isLoggedIn) return
  try {
    const { getOrders } = await import('../api/endpoints')
    const res = await getOrders()
    const paidOrders = res.data.results ? res.data.results.filter(o => o.status === 'paid' || o.status === 'completed') : res.data.filter(o => o.status === 'paid' || o.status === 'completed')
    // Simple check - if user has any paid order, they might have this book
    for (const order of paidOrders) {
      const { getOrderDetail } = await import('../api/endpoints')
      const detail = await getOrderDetail(order.id)
      if (detail.data.items?.some(item => item.book?.id === book.value.id)) {
        purchased.value = true
        return
      }
    }
  } catch (e) {}
}

async function handleFavorite() {
  if (!auth.isLoggedIn) {
    ElMessage.warning('Please login first')
    return
  }
  faving.value = true
  try {
    if (isFaved.value) {
      const { getFavorites } = await import('../api/endpoints')
      const res = await getFavorites()
      const fav = (res.data.results || res.data).find(f => f.book.id === book.value.id)
      if (fav) {
        await removeFavorite(fav.id)
      }
      isFaved.value = false
      ElMessage.success('Removed from favorites')
    } else {
      await addFavorite(book.value.id)
      isFaved.value = true
      ElMessage.success('Added to favorites')
    }
  } catch (e) {
    ElMessage.error('Operation failed')
  }
  faving.value = false
}

async function handleAddToCart() {
  if (!auth.isLoggedIn) {
    ElMessage.warning('Please login first')
    return
  }
  addingCart.value = true
  try {
    await addToCart(book.value.id)
    ElMessage.success('Added to cart')
  } catch (e) {
    ElMessage.error('Failed to add to cart')
  }
  addingCart.value = false
}

async function handleBuy() {
  if (!auth.isLoggedIn) {
    ElMessage.warning('Please login first')
    return
  }
  buying.value = true
  try {
    const res = await createOrder(book.value.id)
    // Auto-pay for demo
    await import('../api/endpoints').then(m => m.payOrder(res.data.id))
    purchased.value = true
    ElMessage.success('Purchase successful! You can now download this book.')
  } catch (e) {
    ElMessage.error('Purchase failed')
  }
  buying.value = false
}

async function handleDownload() {
  downloading.value = true
  try {
    const res = await getBookDownload(book.value.id)
    if (res.data.download_url) {
      window.open(res.data.download_url, '_blank')
      ElMessage.success('Download started!')
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.error || 'Download failed')
  }
  downloading.value = false
}

async function handleRate(val) {
  try {
    await rateBook(book.value.id, val)
    ElMessage.success('Rating submitted!')
  } catch (e) {
    ElMessage.error('Failed to submit rating')
  }
}

onMounted(() => {
  fetchBook().then(() => {
    if (book.value) {
      checkFavorite()
      checkPurchased()
    }
  })
})
</script>

<style scoped>
.book-detail-page {
  max-width: 1000px;
  margin: 0 auto;
}

.loading-box {
  padding: 40px;
}

.book-info {
  display: flex;
  gap: 32px;
  margin-bottom: 40px;
}

.cover-section {
  flex-shrink: 0;
}

.book-cover {
  width: 260px;
  height: 370px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.info-section {
  flex: 1;
}

.info-section h1 {
  font-size: 28px;
  margin-bottom: 8px;
}

.author {
  color: #666;
  font-size: 16px;
  margin-bottom: 16px;
}

.tags {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.price-box {
  margin: 24px 0;
}

.price {
  font-size: 32px;
  color: #f56c6c;
  font-weight: 700;
}

.stats-row {
  display: flex;
  gap: 20px;
  color: #999;
  margin-bottom: 20px;
}

.stats-row span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.download-box {
  margin-top: 16px;
}

.description-section {
  margin-bottom: 40px;
}

.description-section h2 {
  font-size: 20px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 2px solid #ebeef5;
}

.description-section p {
  line-height: 1.8;
  color: #606266;
}

.rating-section {
  margin-bottom: 40px;
}

.rating-section h2 {
  font-size: 20px;
  margin-bottom: 12px;
}

.error-box {
  padding: 100px;
  text-align: center;
}

@media (max-width: 768px) {
  .book-info {
    flex-direction: column;
    align-items: center;
  }
}
</style>
