<template>
  <div class="home-page">
    <!-- Hero Banner -->
    <div class="hero-banner">
      <h1>Discover Your Next Great Read</h1>
      <p>Explore thousands of ebooks across all genres. Find, purchase, and download instantly.</p>
      <el-button type="primary" size="large" @click="$router.push('/books')">Browse All Books</el-button>
    </div>

    <!-- Browse by Category -->
    <section class="section" v-if="categories.length">
      <div class="section-header">
        <h2><el-icon><Collection /></el-icon> Browse by Category</h2>
        <el-button text @click="$router.push('/books')">All Categories <el-icon><ArrowRight /></el-icon></el-button>
      </div>
      <div class="category-grid">
        <div
          v-for="cat in categories"
          :key="cat.id"
          class="category-card"
          @click="$router.push({ path: '/books', query: { category: cat.id } })"
        >
          <span class="cat-name">{{ cat.name }}</span>
          <span class="cat-count">{{ cat.book_count }} books</span>
        </div>
      </div>
    </section>

    <!-- Hot Books -->
    <section class="section">
      <div class="section-header">
        <h2><el-icon><TrendCharts /></el-icon> Hot Books</h2>
        <el-radio-group v-model="hotPeriod" size="small" @change="fetchHotBooks">
          <el-radio-button value="day">Today</el-radio-button>
          <el-radio-button value="week">This Week</el-radio-button>
          <el-radio-button value="all">All Time</el-radio-button>
        </el-radio-group>
      </div>
      <BookGrid :books="hotBooks" :loading="loadingHot" />
    </section>

    <!-- New Books -->
    <section class="section">
      <div class="section-header">
        <h2><el-icon><Star /></el-icon> New Arrivals</h2>
        <el-button text @click="$router.push('/books')">View All <el-icon><ArrowRight /></el-icon></el-button>
      </div>
      <BookGrid :books="newBooks" :loading="loadingNew" />
    </section>

    <!-- Recommended -->
    <section class="section" v-if="auth.isLoggedIn">
      <div class="section-header">
        <h2><el-icon><MagicStick /></el-icon> Recommended For You</h2>
      </div>
      <BookGrid :books="recommendBooks" :loading="loadingRec" />
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getHotBooks, getNewBooks, getRecommendBooks, getCategories } from '../api/endpoints'
import { useAuthStore } from '../store/auth'
import BookGrid from '../components/BookGrid.vue'

const auth = useAuthStore()

const hotBooks = ref([])
const newBooks = ref([])
const recommendBooks = ref([])
const categories = ref([])
const hotPeriod = ref('all')
const loadingHot = ref(false)
const loadingNew = ref(false)
const loadingRec = ref(false)

async function fetchHotBooks() {
  loadingHot.value = true
  try {
    const res = await getHotBooks(hotPeriod.value)
    hotBooks.value = res.data
  } catch (e) {
    hotBooks.value = []
  }
  loadingHot.value = false
}

async function fetchNewBooks() {
  loadingNew.value = true
  try {
    const res = await getNewBooks()
    newBooks.value = res.data
  } catch (e) {
    newBooks.value = []
  }
  loadingNew.value = false
}

async function fetchRecommendBooks() {
  if (!auth.isLoggedIn) return
  loadingRec.value = true
  try {
    const res = await getRecommendBooks()
    recommendBooks.value = res.data
  } catch (e) {
    recommendBooks.value = []
  }
  loadingRec.value = false
}

async function fetchCategories() {
  try {
    const res = await getCategories()
    categories.value = res.data
  } catch (e) { categories.value = [] }
}

onMounted(() => {
  fetchHotBooks()
  fetchNewBooks()
  fetchRecommendBooks()
  fetchCategories()
})
</script>

<style scoped>
.hero-banner {
  background: linear-gradient(135deg, #409eff 0%, #337ecc 100%);
  color: #fff;
  padding: 60px 40px;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 40px;
}

.hero-banner h1 {
  font-size: 36px;
  margin-bottom: 16px;
}

.hero-banner p {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 24px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #303133;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.category-card {
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.category-card:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.15);
  transform: translateY(-2px);
}

.cat-name {
  font-weight: 600;
  font-size: 14px;
  color: #303133;
}

.cat-count {
  font-size: 12px;
  color: #999;
}
</style>
