<template>
  <div class="landing">
    <!-- Section 1: Transparent Navbar -->
    <LandingNav />

    <!-- Section 2: Hero -->
    <section class="hero">
      <div class="hero-content">
        <h1>Discover Books<br /><span class="hero-highlight">You'll Love</span></h1>
        <p>Search, explore, purchase and download e-books across {{ catCount }} categories. Powered by smart recommendations tailored to your taste.</p>
        <div class="hero-stats">
          <div class="stat"><strong>{{ bookCount }}+</strong><span>Books</span></div>
          <div class="stat"><strong>{{ catCount }}</strong><span>Categories</span></div>
        </div>

        <!-- Hero Search Box -->
        <div class="hero-search">
          <el-input
            v-model="heroQuery"
            size="large"
            placeholder="Search by title, author, or keyword..."
            prefix-icon="Search"
            clearable
            @keyup.enter="doHeroSearch"
            class="hero-search-input"
          />
        </div>

        <div class="hero-actions">
          <el-button type="primary" size="large" round @click="$router.push('/books')">Browse Books</el-button>
          <el-button size="large" round class="btn-outline" @click="scrollToPopular">Popular Books</el-button>
        </div>
      </div>
      <div class="hero-glow"></div>
      <div class="hero-scroll-hint" @click="scrollToDiscovery">
        <span>Explore the Store</span>
        <el-icon :size="18"><ArrowDown /></el-icon>
      </div>
    </section>

    <!-- Section 3: Smart Discovery -->
    <section class="section" id="discovery">
      <div class="section-head section-head-center">
        <h2>Smart Discovery</h2>
        <p class="section-subtitle">Discover books through multiple intelligent channels</p>
      </div>
      <div class="discovery-grid">
        <div class="discovery-card">
          <div class="discovery-icon"><el-icon :size="32"><Search /></el-icon></div>
          <h4>Search</h4>
          <p>Find any book instantly by title, author, or keyword across thousands of titles</p>
        </div>
        <div class="discovery-card">
          <div class="discovery-icon"><el-icon :size="32"><TrendCharts /></el-icon></div>
          <h4>Popular Ranking</h4>
          <p>Discover what others are reading — weighted by purchases, favorites, and views</p>
        </div>
        <div class="discovery-card">
          <div class="discovery-icon"><el-icon :size="32"><Star /></el-icon></div>
          <h4>Personalized</h4>
          <p>Get tailored recommendations based on collaborative filtering and your preferences</p>
        </div>
      </div>
    </section>

    <!-- Section 4: Popular Books -->
    <section class="section section-alt" v-if="hotBooks.length" id="popular">
      <div class="section-head">
        <div>
          <h2>Popular Books</h2>
          <p class="section-subtitle">Most purchased and favorited by our readers</p>
        </div>
        <el-button text @click="$router.push('/hot')">View All <el-icon><ArrowRight /></el-icon></el-button>
      </div>
      <div class="book-grid">
        <div v-for="book in hotBooks" :key="book.id" class="book-card" @click="$router.push(`/books/${book.id}`)">
          <img :src="book.cover_url" :alt="book.title" @error="e=>e.target.src='https://picsum.photos/200/300'" />
          <div class="book-card-info">
            <h4>{{ book.title }}</h4>
            <span class="book-author">{{ book.author }}</span>
            <span class="book-price">${{ book.price }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 5: Recommended For You -->
    <section class="section section-alt" v-if="recBooks.length">
      <div class="section-head">
        <div>
          <h2>Recommended For You</h2>
          <p class="section-subtitle">Personalized picks powered by collaborative filtering</p>
        </div>
        <el-button text @click="$router.push('/recommended')">View All <el-icon><ArrowRight /></el-icon></el-button>
      </div>
      <div class="book-grid">
        <div v-for="book in recBooks" :key="book.id" class="book-card" @click="$router.push(`/books/${book.id}`)">
          <img :src="book.cover_url" :alt="book.title" @error="e=>e.target.src='https://picsum.photos/200/300'" />
          <div class="book-card-info">
            <h4>{{ book.title }}</h4>
            <span class="book-author">{{ book.author }}</span>
            <span class="book-price">${{ book.price }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 6: Footer -->
    <footer class="landing-footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <h3>EBookStore</h3>
          <p>Your digital bookstore — discover, collect, purchase, and download the books you love.</p>
        </div>
        <div class="footer-links">
          <div class="footer-col">
            <h4>Explore</h4>
            <router-link to="/books">Browse All</router-link>
            <router-link to="/hot">Popular</router-link>
            <router-link to="/recommended">Recommended</router-link>
          </div>
          <div class="footer-col">
            <h4>Account</h4>
            <router-link to="/login">Sign In</router-link>
            <router-link to="/register">Create Account</router-link>
            <router-link to="/profile">Profile</router-link>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 EBookStore. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getHotBooks, getRecommendBooks, getCategories, getBooks } from '../api/endpoints'
import LandingNav from '../components/LandingNav.vue'

const router = useRouter()

const hotBooks = ref([])
const recBooks = ref([])
const categories = ref([])
const bookCount = ref(0)
const catCount = ref(0)
const heroQuery = ref('')

function doHeroSearch() {
  const q = heroQuery.value.trim()
  if (q) router.push({ name: 'Search', query: { q } })
}

function scrollToDiscovery() {
  document.getElementById('discovery')?.scrollIntoView({ behavior: 'smooth' })
}

function scrollToPopular() {
  document.getElementById('popular')?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(async () => {
  try {
    const [hot, rec, cat, books] = await Promise.all([
      getHotBooks('all'),
      getRecommendBooks(),
      getCategories(),
      getBooks({ page: 1 }),
    ])
    hotBooks.value = (hot.data || []).slice(0, 8)
    recBooks.value = (rec.data || []).slice(0, 8)
    categories.value = cat.data || []
    catCount.value = categories.value.length
    bookCount.value = books.data.count || 1000
  } catch (e) {}
})
</script>

<style scoped>
/* ══════════════════════════════════════════════════════════════
   Premium Light-Mode Theme — EBookStore HomePage
   Palette: White / Ice-Blue / Charcoal / Sky-Blue Accent
   ══════════════════════════════════════════════════════════════ */

/* ── LandingNav Override: light-mode glassmorphism ── */
:deep(.landing-nav) {
  background: rgba(255,255,255,0.72) !important;
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border-bottom: 1px solid rgba(0,0,0,0.06);
}
:deep(.nav-brand)        { color: #0f172a !important; }
:deep(.nav-link)         { color: #475569 !important; }
:deep(.nav-link:hover)   { color: #2563eb !important; }
:deep(.nav-icon-btn)     { color: #475569 !important; background: transparent !important; }
:deep(.nav-icon-btn:hover) { color: #2563eb !important; background: rgba(37,99,235,0.06) !important; }
:deep(.nav-item)         { color: #475569 !important; }
:deep(.nav-item:hover)   { color: #2563eb !important; background: rgba(37,99,235,0.05) !important; }
:deep(.nav-item--active) { color: #2563eb !important; background: rgba(37,99,235,0.08) !important; }
:deep(.nav-user-btn) {
  color: #0f172a !important;
  background: rgba(37,99,235,0.05) !important;
  border: 1px solid #e2e8f0 !important;
}
:deep(.nav-user-btn:hover) {
  color: #2563eb !important;
  background: rgba(37,99,235,0.08) !important;
  border-color: #2563eb !important;
}

/* ── Layout Reset ── */
.landing {
  width: 100%; min-height: 100vh; min-height: 100dvh;
  display: flex; flex-direction: column;
  overflow-x: hidden;
  background: #ffffff;
}

/* ═══ Hero — Light Gradient Full-Screen · 3‑Zone Artistic Layout ═══ */
.hero {
  width: 100%; min-height: 100vh; min-height: 100dvh;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(170deg, #f8fafc 0%, #fafbfd 25%, #eff6ff 60%, #f4f7fb 100%);
  position: relative; overflow: hidden;
  flex-shrink: 0;
}
/* primary glow — top‑right ambient orb */
.hero-glow {
  position: absolute; top: -220px; right: -140px;
  width: 680px; height: 680px;
  background: radial-gradient(circle, rgba(37,99,235,0.06) 0%, rgba(59,130,246,0.025) 45%, transparent 72%);
  pointer-events: none;
}
/* secondary glow — bottom‑left whisper for visual balance */
.hero::after {
  content: ''; position: absolute; bottom: -160px; left: -80px;
  width: 480px; height: 480px;
  background: radial-gradient(circle, rgba(148,163,184,0.05) 0%, rgba(203,213,225,0.02) 40%, transparent 70%);
  pointer-events: none;
}

/* ── Content wrapper: zone‑based vertical rhythm ── */
.hero-content {
  position: relative; z-index: 1;
  max-width: 840px; margin: 0 auto; padding: 110px 28px 72px;
  text-align: center; display: flex; flex-direction: column; align-items: center;
  gap: 0; /* manual margins for precise zonal rhythm */
}

/* ═══ Zone 1 · Message ═══ */
.hero-content h1 {
  font-size: clamp(34px, 5.5vw, 62px); font-weight: 800;
  color: #0f172a; line-height: 1.12; letter-spacing: -1.8px; margin: 0 0 18px;
}
.hero-highlight {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #60a5fa 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-content > p {
  font-size: 17px; color: #475569; max-width: 540px; margin: 0 0 42px;
  line-height: 1.65; font-weight: 400;
}

/* ═══ Zone 2 · Proof — clean stat bar ═══ */
.hero-stats {
  display: flex; gap: 48px;
  margin-bottom: 46px;
}
.stat { display: flex; flex-direction: column; align-items: center; gap: 1px; }
.stat strong { font-size: 30px; font-weight: 700; color: #2563eb; letter-spacing: -0.5px; }
.stat span  { font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 500; }

/* ═══ Zone 3 · Action — search + ctas ═══ */
.hero-search { width: min(580px, 88vw); margin-bottom: 18px; }
.hero-search-input :deep(.el-input__wrapper) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 30px; padding: 5px 22px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.035), 0 1px 2px rgba(0,0,0,0.03);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.hero-search-input :deep(.el-input__wrapper:hover) {
  border-color: #cbd5e1;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.04);
}
.hero-search-input :deep(.el-input__wrapper.is-focus) {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.09), 0 2px 12px rgba(0,0,0,0.05);
}
.hero-search-input :deep(.el-input__inner) { color: #1e293b; font-size: 15px; }
.hero-search-input :deep(.el-input__inner::placeholder) { color: #94a3b8; }
.hero-search-input :deep(.el-input__prefix) { color: #94a3b8; }
.hero-search-input :deep(.el-input__clear) { color: #94a3b8; }

.hero-actions {
  display: flex; gap: 15px; flex-wrap: wrap; justify-content: center;
  margin-bottom: 0;
}
.btn-outline {
  background: transparent !important;
  border: 1px solid #cbd5e1 !important;
  color: #334155 !important;
  font-weight: 500 !important;
}
.btn-outline:hover {
  border-color: #2563eb !important;
  color: #2563eb !important;
  background: rgba(37,99,235,0.04) !important;
}

/* ── Scroll Hint — absolute bottom, always visible ── */
.hero-scroll-hint {
  position: absolute; bottom: 32px; left: 0; right: 0;
  margin: 0 auto; width: fit-content;
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  cursor: pointer; color: #94a3b8; z-index: 2;
  transition: color 0.3s; user-select: none;
}
.hero-scroll-hint:hover { color: #2563eb; }
.hero-scroll-hint span { font-size: 11px; letter-spacing: 1.2px; text-transform: uppercase; font-weight: 500; }
.hero-scroll-hint .el-icon { animation: bounce 2s infinite; }
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(6px); }
}

/* ═══ Sections — Elegant Alternating Rhythm ═══ */
.section {
  max-width: 1280px; margin: 0 auto; padding: 80px 24px;
}
.section-alt {
  background: #f8fafc; max-width: none;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
}
.section-alt > * { max-width: 1280px; margin-left: auto; margin-right: auto; }
.section-head {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 36px;
}
.section-head h2 {
  font-size: 28px; font-weight: 700; color: #0f172a; margin: 0 0 4px;
  letter-spacing: -0.5px;
}
.section-head-center { text-align: center; flex-direction: column; }
.section-subtitle { font-size: 14px; color: #64748b; margin: 0; line-height: 1.5; }

/* ═══ Smart Discovery Cards ═══ */
.discovery-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.discovery-card {
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 16px;
  padding: 36px 28px; text-align: center;
  box-shadow: 0 1px 2px 0 rgba(0,0,0,0.03);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.discovery-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.06), 0 2px 6px rgba(0,0,0,0.03);
  border-color: #e2e8f0;
}
.discovery-icon {
  width: 64px; height: 64px; border-radius: 16px;
  background: rgba(37,99,235,0.06); color: #2563eb;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
}
.discovery-card h4 { font-size: 17px; font-weight: 600; color: #0f172a; margin: 0 0 8px; }
.discovery-card p  { font-size: 14px; color: #64748b; line-height: 1.6; margin: 0; }

/* ═══ Book Cards — Refined Elevation ═══ */
.book-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}
.book-card {
  cursor: pointer; border-radius: 16px;
  background: #fff; border: 1px solid #f1f5f9;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 1px 2px rgba(0,0,0,0.04);
  transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.book-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 32px rgba(0,0,0,0.08), 0 4px 10px rgba(0,0,0,0.04);
  border-color: #e2e8f0;
}
.book-card img {
  width: 100%; aspect-ratio: 2/3; object-fit: cover; display: block;
  background: #f8fafc;
}
.book-card-info { padding: 16px; }
.book-card-info h4 {
  font-size: 14px; font-weight: 600; color: #1e293b;
  margin: 0 0 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  line-height: 1.3;
}
.book-author { font-size: 13px; color: #94a3b8; display: block; margin-bottom: 10px; }
.book-price { font-size: 16px; font-weight: 700; color: #0f172a; }

/* ═══ Footer — Anchored Dark ═══ */
.landing-footer { margin-top: auto; background: #0f172a; color: #cbd5e1; padding: 56px 24px 28px; }
.footer-inner { max-width: 1280px; margin: 0 auto; display: flex; gap: 64px; flex-wrap: wrap; margin-bottom: 40px; }
.footer-brand { max-width: 320px; }
.footer-brand h3 { color: #fff; font-size: 20px; margin: 0 0 8px; }
.footer-brand p { color: #94a3b8; font-size: 14px; line-height: 1.6; margin: 0; }
.footer-links { display: flex; gap: 64px; }
.footer-col h4 { color: #fff; font-size: 14px; margin: 0 0 12px; text-transform: uppercase; letter-spacing: 0.5px; }
.footer-col a { display: block; color: #94a3b8; font-size: 14px; margin-bottom: 8px; transition: color 0.2s; }
.footer-col a:hover { color: #fff; }
.footer-bottom { max-width: 1280px; margin: 0 auto; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.08); text-align: center; }
.footer-bottom p { color: #64748b; font-size: 13px; margin: 0; }

/* ═══ Responsive ═══ */
@media (max-width: 1024px) {
  .book-grid { grid-template-columns: repeat(3, 1fr); gap: 20px; }
}
@media (max-width: 768px) {
  .discovery-grid { grid-template-columns: repeat(1, 1fr); gap: 16px; }
  .book-grid { grid-template-columns: repeat(2, 1fr); gap: 16px; }
  .hero-content { padding: 100px 24px 64px; }
  .hero-content > p { margin-bottom: 34px; }
  .hero-stats { margin-bottom: 36px; gap: 36px; }
  .hero-scroll-hint { bottom: 26px; }
}
@media (max-width: 640px) {
  .hero-content { padding: 88px 20px 56px; }
  .hero-content h1 { font-size: clamp(28px, 8vw, 42px); letter-spacing: -1.2px; margin-bottom: 14px; }
  .hero-content > p { font-size: 15px; margin-bottom: 28px; max-width: 100%; }
  .hero-stats { gap: 28px; margin-bottom: 30px; }
  .stat strong { font-size: 26px; }
  .hero-search { width: 100%; margin-bottom: 14px; }
  .hero-scroll-hint { bottom: 20px; }
  .hero-scroll-hint span { font-size: 10px; }
  .footer-inner { flex-direction: column; gap: 32px; }
  .footer-links { gap: 32px; }
}
</style>
