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
            <template v-if="!purchased">
              <el-button type="primary" size="large" @click="handleBuy" :loading="buying">Buy Now</el-button>
              <el-button size="large" @click="handleAddToCart" :loading="addingCart">Add to Cart</el-button>
            </template>
            <el-tag v-else type="success" size="large">Purchased</el-tag>
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

      <!-- Rating & Review (purchased users only) -->
      <div class="review-section" v-if="purchased">
        <h2>{{ hasSubmitted ? 'Your Review' : 'Write a Review' }}</h2>
        <div class="rating-input">
          <el-rate
            v-model="userRating"
            :texts="['Poor', 'Fair', 'Good', 'Great', 'Excellent']"
            show-text
          />
        </div>
        <el-input
          v-model="userReview"
          type="textarea"
          :rows="3"
          placeholder="Share your thoughts about this book..."
        />
        <div class="review-submit-bar">
          <span class="review-hint" v-if="!hasSubmitted && userRating === 0">Select a star rating to begin</span>
          <span class="review-hint" v-else-if="!hasSubmitted">{{ submitHint }}</span>
          <span class="review-hint submitted" v-else>✓ Review submitted</span>
          <el-button
            type="primary"
            :disabled="userRating === 0"
            :loading="submitting"
            @click="handleSubmitReview"
          >
            {{ hasSubmitted ? 'Update' : 'Submit Review' }}
          </el-button>
        </div>
      </div>

      <!-- All Reviews -->
      <div class="reviews-list">
        <h2>Reviews ({{ reviews.length }})</h2>
        <div v-if="reviews.length === 0" class="no-reviews">
          <el-empty description="No reviews yet" :image-size="80" />
        </div>
        <div v-for="r in reviews" :key="r.id" class="review-item">
          <div class="review-header">
            <span class="review-user">{{ r.user }}</span>
            <el-rate :model-value="r.rating" disabled show-score text-color="#ff9900" />
            <span class="review-date">{{ new Date(r.created_at).toLocaleDateString() }}</span>
          </div>
          <p v-if="r.review" class="review-text">{{ r.review }}</p>
        </div>
      </div>

      <!-- You Might Also Like -->
      <div class="recommended-section" v-if="recBooks.length">
        <h2>You Might Also Like</h2>
        <p class="rec-subtitle">Powered by KNN collaborative filtering</p>
        <div class="rec-grid">
          <div v-for="rb in recBooks" :key="rb.id" class="rec-card" @click="$router.push(`/books/${rb.id}`)">
            <img :src="rb.cover_url" :alt="rb.title" @error="e => e.target.src='https://picsum.photos/seed/default/200/300'" />
            <div class="rec-info">
              <h4>{{ rb.title }}</h4>
              <span>{{ rb.author }}</span>
              <strong>${{ rb.price }}</strong>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="error-box">
      <el-empty description="Book not found" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getBookDetail, addFavorite, removeFavorite, addToCart, createOrder, getBookDownload, getFavorites, rateBook, getBookReviews, getRecommendBooks } from '../api/endpoints'
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
const userReview = ref('')
const reviews = ref([])
const hasSubmitted = ref(false)
const submitting = ref(false)
const recBooks = ref([])

const submitHint = computed(() => {
  if (userRating.value === 0) return 'Select a star rating to begin'
  const texts = ['', 'Poor', 'Fair', 'Good', 'Great', 'Excellent']
  return `Ready to submit: "${texts[userRating.value]}" — click the button`
})

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

async function fetchReviews() {
  try {
    const res = await getBookReviews(route.params.id)
    reviews.value = res.data
    // Check if current user already rated/reviewed
    if (auth.isLoggedIn) {
      const myReview = res.data.find(r => r.user === auth.user?.username)
      if (myReview) {
        userRating.value = myReview.rating
        userReview.value = myReview.review || ''
        hasSubmitted.value = true
      }
    }
  } catch (e) {}
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
      if (fav) await removeFavorite(fav.id)
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
    ElMessage.error(e.response?.data?.error || 'Failed to add to cart')
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
    await import('../api/endpoints').then(m => m.payOrder(res.data.id))
    purchased.value = true
    ElMessage.success('Purchase successful! You can now rate and review this book.')
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

async function handleSubmitReview() {
  if (userRating.value === 0) return
  submitting.value = true
  const isUpdate = hasSubmitted.value
  try {
    await rateBook(book.value.id, userRating.value, userReview.value)
    hasSubmitted.value = true
    ElMessage.success(isUpdate ? 'Review updated!' : 'Review submitted!')
    fetchReviews()
  } catch (e) {
    ElMessage.error(e.response?.data?.error || 'Failed to submit review')
  }
  submitting.value = false
}

async function fetchRecommended() {
  try {
    const res = await getRecommendBooks()
    recBooks.value = (res.data || []).filter(b => b.id !== Number(route.params.id)).slice(0, 4)
  } catch (e) {}
}

onMounted(() => {
  fetchBook().then(() => {
    if (book.value) {
      checkFavorite()
      checkPurchased()
      fetchReviews()
      fetchRecommended()
    }
  })
})
</script>

<style scoped>
.book-detail-page { max-width: 1000px; margin: 0 auto; padding: 0 32px; }
.loading-box { padding: 40px; }
.book-info { display: flex; gap: 36px; margin-bottom: 44px; }
.cover-section { flex-shrink: 0; }
.book-cover { width: 260px; height: 370px; object-fit: cover; border-radius: 10px; box-shadow: 0 4px 24px rgba(0,0,0,0.10); }
.info-section { flex: 1; }
.info-section h1 { font-size: 28px; font-weight: 700; color: #1a1815; margin-bottom: 36px; letter-spacing: -0.5px; }
.author { color: #8b7e74; font-size: 16px; margin-bottom: 16px; }
.tags { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 6px; }
.price-box { margin: 24px 0; }
.price { font-size: 32px; color: #1a1815; font-weight: 700; }
.stats-row { display: flex; gap: 20px; color: #a0988c; margin-bottom: 20px; }
.stats-row span { display: flex; align-items: center; gap: 4px; }
.actions { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
.download-box { margin-top: 16px; }
.description-section { margin-bottom: 44px; }
.description-section { margin-bottom: 44px; }
.description-section h2 { font-size: 22px; font-weight: 600; color: #1a1815; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid #f0f0f0; }
.description-section p { line-height: 1.8; color: #4a4038; max-width: 680px; }

.review-section { margin-bottom: 36px; }
.review-section h2 { font-size: 22px; font-weight: 600; color: #1a1815; margin-bottom: 14px; }
.rating-input { margin-bottom: 12px; }

.review-submit-bar {
  display: flex; align-items: center; justify-content: space-between;
  margin-top: 12px; gap: 16px;
}
.review-hint { font-size: 13px; color: #a0988c; transition: color 0.3s; }
.review-hint.submitted { color: #10b981; font-weight: 500; }

.reviews-list h2 { font-size: 22px; font-weight: 600; color: #1a1815; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px solid #f0f0f0; }
.no-reviews { padding: 20px 0; }
.review-item { padding: 18px 0; border-bottom: 1px solid #f0f0f0; }
.review-item:last-child { border-bottom: none; }
.review-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.review-user { font-weight: 600; color: #1a1815; }
.review-date { color: #a0988c; font-size: 13px; margin-left: auto; }
.review-text { color: #4a4038; line-height: 1.6; margin: 0; }

.error-box { padding: 100px; text-align: center; }

.recommended-section {
  margin-top: 48px; padding-top: 36px;
  border-top: 1px solid #f0f0f0;
}
.recommended-section h2 { font-size: 22px; font-weight: 600; color: #1a1815; margin-bottom: 6px; }
.rec-subtitle { font-size: 13px; color: #a0988c; margin: 0 0 22px; }
.rec-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.rec-card {
  cursor: pointer; border-radius: 10px; overflow: hidden;
  background: transparent; border: none;
  transition: transform 0.3s ease;
}
.rec-card:hover { transform: translateY(-3px); }
.rec-card:hover img { box-shadow: 0 6px 20px rgba(0,0,0,0.10); }
.rec-card img {
  width: 100%; aspect-ratio: 2/3; object-fit: cover; display: block;
  border-radius: 10px; background: #f0f0f0;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  transition: box-shadow 0.3s ease;
}
.rec-info { padding: 12px 4px 0; }
.rec-info h4 { font-size: 13px; font-weight: 600; color: #1e1b18; margin: 0 0 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.rec-info span { font-size: 12px; color: #a0988c; display: block; margin-bottom: 6px; }
.rec-info strong { font-size: 14px; font-weight: 700; color: #1a1815; }

@media (max-width: 768px) {
  .book-info { flex-direction: column; align-items: center; }
  .rec-grid { grid-template-columns: repeat(2, 1fr); }
  .book-cover { width: 200px; height: 285px; }
  .review-header { flex-wrap: wrap; }
}
@media (max-width: 480px) {
  .book-detail-page { padding: 0 16px; }
  .book-cover { width: 160px; height: 228px; }
  .rec-grid { grid-template-columns: repeat(1, 1fr); }
  .info-section h1 { font-size: 24px; }
  .actions { flex-direction: column; align-items: stretch; }
  .review-submit-bar { flex-direction: column; align-items: stretch; }
}
</style>
