<template>
  <div class="home-page">
    <!-- Full-screen Hero (80vh) -->
    <section class="hero-fullscreen">
      <div class="hero-body">
        <h1 class="hero-logo">EBookStore</h1>
        <p class="hero-tagline">Your Infinite Library, One Click Away</p>
        <p class="hero-desc">Thousands of titles across every genre. Read, discover, and collect the books you love.</p>
        <div class="hero-cta" v-if="!auth.isLoggedIn">
          <el-button type="primary" size="large" round @click="$router.push('/register')">Start Reading Free</el-button>
          <el-button size="large" round class="hero-btn-outline" @click="$router.push('/books')">Browse Collection</el-button>
        </div>
        <div class="hero-cta" v-else>
          <el-button type="primary" size="large" round @click="$router.push('/books')">Browse Collection</el-button>
        </div>
        <div class="scroll-hint" @click="scrollDown">
          <span>Explore</span>
          <el-icon :size="20"><ArrowDown /></el-icon>
        </div>
      </div>
      <div class="hero-bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
      </div>
    </section>

    <!-- 4 Vertical Feature Panels -->
    <section class="panels-section">
      <div class="panel panel-browse" @click="$router.push('/books')">
        <div class="panel-inner">
          <div class="panel-icon-wrap"><el-icon :size="40"><Collection /></el-icon></div>
          <div class="panel-text">
            <h2>Browse All Books</h2>
            <p>Explore our complete library of {{ bookCount }}+ titles across {{ catCount }} categories — from computer science to classic literature.</p>
            <span class="panel-cta">View Full Library <el-icon><ArrowRight /></el-icon></span>
          </div>
        </div>
      </div>
      <div class="panel panel-new" @click="$router.push('/new')">
        <div class="panel-inner">
          <div class="panel-icon-wrap"><el-icon :size="40"><Star /></el-icon></div>
          <div class="panel-text">
            <h2>New Arrivals</h2>
            <p>Fresh off the shelf — be the first to discover newly added books and emerging authors.</p>
            <span class="panel-cta">See What's New <el-icon><ArrowRight /></el-icon></span>
          </div>
        </div>
      </div>
      <div class="panel panel-hot" @click="$router.push('/hot')">
        <div class="panel-inner">
          <div class="panel-icon-wrap"><el-icon :size="40"><TrendCharts /></el-icon></div>
          <div class="panel-text">
            <h2>Hot & Trending</h2>
            <p>What the community is reading right now — ranked by real-time popularity and engagement.</p>
            <span class="panel-cta">View Trending <el-icon><ArrowRight /></el-icon></span>
          </div>
        </div>
      </div>
      <div class="panel panel-recommend" @click="$router.push('/recommended')">
        <div class="panel-inner">
          <div class="panel-icon-wrap"><el-icon :size="40"><MagicStick /></el-icon></div>
          <div class="panel-text">
            <h2>Recommended For You</h2>
            <p>AI-powered personalized recommendations based on your taste, ratings, and reading history.</p>
            <span class="panel-cta">Get Recommendations <el-icon><ArrowRight /></el-icon></span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategories, getBooks } from '../api/endpoints'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const bookCount = ref(0)
const catCount = ref(0)

function scrollDown() {
  document.querySelector('.panels-section')?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(async () => {
  try {
    const [catRes, bookRes] = await Promise.all([getCategories(), getBooks({ page: 1 })])
    catCount.value = (catRes.data || []).length
    bookCount.value = bookRes.data.count || 1000
  } catch (e) {}
})
</script>

<style scoped>
/* ── Full-width Hero (80vh) ── */
.hero-fullscreen {
  width: 100%;
  min-height: 80vh;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  position: relative;
  background: linear-gradient(160deg, #080d1f 0%, #0f1d3a 40%, #0d1830 70%, #080d1f 100%);
  overflow: hidden;
  margin-top: -64px;  /* overlap under transparent header */
  padding-top: 64px;
}
.hero-bg-shapes {
  position: absolute; inset: 0; pointer-events: none; z-index: 0;
}
.shape {
  position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.12;
}
.shape-1 { width: 600px; height: 600px; background: #409eff; top: -200px; right: -150px; }
.shape-2 { width: 400px; height: 400px; background: #2563eb; bottom: -120px; left: -100px; }

/* Hero body */
.hero-body {
  position: relative; z-index: 1;
  display: flex; flex-direction: column;
  justify-content: center; align-items: center;
  text-align: center;
  padding: 0 24px 60px;
  max-width: 900px;
  width: 100%;
}
.hero-logo {
  font-size: clamp(48px, 8vw, 88px);
  font-weight: 900; color: #fff; margin: 0 0 16px;
  letter-spacing: -2px;
  background: linear-gradient(135deg, #409eff 0%, #a5d8ff 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-tagline {
  font-size: clamp(18px, 3vw, 28px);
  color: rgba(255,255,255,0.85); margin: 0 0 12px;
  font-weight: 400; max-width: 600px;
}
.hero-desc {
  font-size: 16px; color: rgba(255,255,255,0.55);
  margin: 0 0 40px; max-width: 480px;
}
.hero-cta { display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; }
.hero-btn-outline {
  background: transparent !important;
  border: 1px solid rgba(255,255,255,0.25) !important;
  color: #fff !important;
}
.hero-btn-outline:hover { border-color: rgba(255,255,255,0.5) !important; }

/* Scroll hint */
.scroll-hint {
  position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  color: rgba(255,255,255,0.35); cursor: pointer; transition: color 0.3s;
  z-index: 2;
}
.scroll-hint:hover { color: rgba(255,255,255,0.65); }
.scroll-hint span { font-size: 12px; text-transform: uppercase; letter-spacing: 2px; font-weight: 500; }
.scroll-hint .el-icon { animation: bounce 2s infinite; }
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(6px); }
}

/* ── 4 Vertical Panels ── */
.panels-section {
  padding: 60px 0 40px;
  display: flex; flex-direction: column;
  align-items: center;
  background: #fff;
  position: relative; z-index: 1;
}
.panels-section .panel {
  max-width: 960px; width: 100%;
}
.panel {
  cursor: pointer; transition: all 0.35s;
  border-radius: 0; position: relative;
}
.panel:first-child { border-radius: 16px 16px 0 0; }
.panel:last-child { border-radius: 0 0 16px 16px; }
.panel:not(:last-child) { border-bottom: 1px solid #ebeef5; }
.panel:hover { background: #f8fafc; padding-left: 12px; }
.panel-inner {
  display: flex; align-items: center; gap: 28px;
  padding: 32px 36px;
}
.panel-icon-wrap {
  width: 72px; height: 72px; border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.panel-browse .panel-icon-wrap { background: #ecf5ff; color: #409eff; }
.panel-new .panel-icon-wrap { background: #f0f9eb; color: #67c23a; }
.panel-hot .panel-icon-wrap { background: #fdf6ec; color: #e6a23c; }
.panel-recommend .panel-icon-wrap { background: #fef0f0; color: #f56c6c; }
.panel-text { flex: 1; }
.panel-text h2 { font-size: 22px; font-weight: 700; color: #1e293b; margin: 0 0 6px; }
.panel-text p { color: #64748b; font-size: 15px; line-height: 1.6; margin: 0 0 10px; }
.panel-cta {
  color: #409eff; font-weight: 600; font-size: 14px;
  display: inline-flex; align-items: center; gap: 4px;
}
.panel:hover .panel-cta { gap: 8px; transition: gap 0.3s; }

@media (max-width: 640px) {
  .panel-inner { flex-direction: column; text-align: center; padding: 24px 20px; }
  .panel-icon-wrap { width: 56px; height: 56px; }
}
</style>
