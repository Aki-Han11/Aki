<template>
  <div class="home-page">
    <!-- Hero Banner -->
    <section class="hero">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <h1 class="hero-title">EBookStore</h1>
        <p class="hero-subtitle">Discover thousands of books. Read anywhere, anytime.</p>
        <div class="hero-stats">
          <div class="stat-item"><span class="stat-num">{{ bookCount }}+</span><span class="stat-label">Books</span></div>
          <div class="stat-item"><span class="stat-num">{{ catCount }}+</span><span class="stat-label">Categories</span></div>
          <div class="stat-item"><span class="stat-num">{{ userCount }}+</span><span class="stat-label">Readers</span></div>
        </div>
      </div>
    </section>

    <!-- Login / Register prompt (not logged in) -->
    <section v-if="!auth.isLoggedIn" class="auth-callout">
      <div class="auth-card">
        <h2>Start Your Reading Journey</h2>
        <p>Sign in to browse personalized recommendations, save favorites, and purchase books.</p>
        <div class="auth-buttons">
          <el-button type="primary" size="large" round @click="$router.push('/login')">Sign In</el-button>
          <el-button size="large" round @click="$router.push('/register')">Create Account</el-button>
        </div>
      </div>
    </section>

    <!-- 4 Feature Panels (logged in) -->
    <section v-else class="feature-panels">
      <div class="panel-grid">
        <div class="panel panel-browse" @click="$router.push('/books')">
          <div class="panel-icon"><el-icon :size="48"><Collection /></el-icon></div>
          <h3>Browse All</h3>
          <p>Explore our complete collection of {{ bookCount }}+ ebooks across {{ catCount }} categories</p>
          <span class="panel-link">View Library <el-icon><ArrowRight /></el-icon></span>
        </div>
        <div class="panel panel-new" @click="$router.push('/new')">
          <div class="panel-icon"><el-icon :size="48"><Star /></el-icon></div>
          <h3>New Arrivals</h3>
          <p>Be the first to discover newly added books fresh off the press</p>
          <span class="panel-link">See What's New <el-icon><ArrowRight /></el-icon></span>
        </div>
        <div class="panel panel-hot" @click="$router.push('/hot')">
          <div class="panel-icon"><el-icon :size="48"><TrendCharts /></el-icon></div>
          <h3>Hot Books</h3>
          <p>What everyone is reading — trending books ranked by popularity</p>
          <span class="panel-link">View Trending <el-icon><ArrowRight /></el-icon></span>
        </div>
        <div class="panel panel-recommend" @click="$router.push('/recommended')">
          <div class="panel-icon"><el-icon :size="48"><MagicStick /></el-icon></div>
          <h3>Recommended For You</h3>
          <p>Personalized picks based on your reading history and ratings</p>
          <span class="panel-link">Get Recommendations <el-icon><ArrowRight /></el-icon></span>
        </div>
      </div>
    </section>

    <!-- Browse by Category -->
    <section class="section" v-if="categories.length">
      <div class="section-header">
        <h2>Browse by Category</h2>
        <el-button text @click="$router.push('/books')">All Categories <el-icon><ArrowRight /></el-icon></el-button>
      </div>
      <div class="category-grid">
        <div v-for="cat in categories" :key="cat.id" class="category-card"
             @click="$router.push({path:'/books',query:{category:cat.id}})">
          <span class="cat-name">{{ cat.name }}</span>
          <span class="cat-count">{{ cat.book_count }} books</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getCategories, getBooks } from '../api/endpoints'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const categories = ref([])
const bookCount = ref(0)
const catCount = ref(0)
const userCount = ref(50)

async function fetchData() {
  try {
    const [catRes, bookRes] = await Promise.all([
      getCategories(),
      getBooks({ page: 1 }),
    ])
    categories.value = catRes.data || []
    catCount.value = categories.value.length
    bookCount.value = bookRes.data.count || 1000
  } catch (e) {}
}

onMounted(fetchData)
</script>

<style scoped>
/* Hero */
.hero {
  position: relative;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 70%, #1a1a2e 100%);
  padding: 100px 40px 80px;
  text-align: center;
  border-radius: 16px;
  margin-bottom: 40px;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: radial-gradient(circle at 30% 40%, rgba(64,158,255,0.08) 0%, transparent 50%),
              radial-gradient(circle at 70% 60%, rgba(245,108,108,0.06) 0%, transparent 50%);
  animation: heroPulse 8s ease-in-out infinite;
}
@keyframes heroPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}
.hero-content { position: relative; z-index: 1; }
.hero-title {
  font-size: 64px; font-weight: 800; color: #fff; margin: 0 0 16px;
  letter-spacing: -1px; background: linear-gradient(135deg, #409eff, #67c23a);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-subtitle { font-size: 20px; color: rgba(255,255,255,0.7); margin-bottom: 40px; max-width: 500px; margin-left: auto; margin-right: auto; }
.hero-stats { display: flex; justify-content: center; gap: 48px; }
.stat-item { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.stat-num { font-size: 32px; font-weight: 700; color: #409eff; }
.stat-label { font-size: 14px; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px; }

/* Auth CTA */
.auth-callout { margin-bottom: 40px; }
.auth-card {
  background: linear-gradient(135deg, #f0f5ff, #e6f7ff);
  border-radius: 16px; padding: 48px 40px; text-align: center;
  border: 1px solid #d6e4ff;
}
.auth-card h2 { font-size: 28px; color: #303133; margin-bottom: 12px; }
.auth-card p { color: #666; font-size: 16px; margin-bottom: 28px; max-width: 450px; margin-left: auto; margin-right: auto; }
.auth-buttons { display: flex; gap: 16px; justify-content: center; }

/* 4 Feature Panels */
.feature-panels { margin-bottom: 40px; }
.panel-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
.panel {
  background: #fff;
  border-radius: 14px;
  padding: 36px 28px 28px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #ebeef5;
  position: relative;
  overflow: hidden;
}
.panel::after {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 4px;
  transition: all 0.3s;
}
.panel-browse::after { background: #409eff; }
.panel-new::after { background: #67c23a; }
.panel-hot::after { background: #e6a23c; }
.panel-recommend::after { background: #f56c6c; }
.panel:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.1);
}
.panel-icon { margin-bottom: 16px; }
.panel-browse .panel-icon { color: #409eff; }
.panel-new .panel-icon { color: #67c23a; }
.panel-hot .panel-icon { color: #e6a23c; }
.panel-recommend .panel-icon { color: #f56c6c; }
.panel h3 { font-size: 20px; font-weight: 700; color: #303133; margin-bottom: 8px; }
.panel p { color: #909399; font-size: 14px; line-height: 1.6; margin-bottom: 16px; }
.panel-link {
  color: #409eff; font-weight: 600; font-size: 14px;
  display: inline-flex; align-items: center; gap: 4px;
}

/* Categories */
.section { margin-bottom: 40px; }
.section-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 20px;
}
.section-header h2 { font-size: 24px; color: #303133; }
.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}
.category-card {
  background: #fff; border: 1px solid #ebeef5; border-radius: 8px;
  padding: 16px; cursor: pointer; transition: all 0.2s;
  text-align: center; display: flex; flex-direction: column; gap: 4px;
}
.category-card:hover { border-color: #409eff; box-shadow: 0 2px 8px rgba(64,158,255,0.15); transform: translateY(-2px); }
.cat-name { font-weight: 600; font-size: 14px; color: #303133; }
.cat-count { font-size: 12px; color: #999; }

@media (max-width: 900px) {
  .panel-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 560px) {
  .panel-grid { grid-template-columns: 1fr; }
  .hero-title { font-size: 40px; }
}
</style>
