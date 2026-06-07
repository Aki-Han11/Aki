<template>
  <div class="landing">
    <!-- Section 1: Transparent Navbar -->
    <LandingNav />

    <!-- Section 2: Hero — "Air & Light" design -->
    <section class="hero">
      <!-- Abstract geometric floating shapes -->
      <div class="hero-shapes">
        <div class="hero-shape shape-1"></div>
        <div class="hero-shape shape-2"></div>
        <div class="hero-shape shape-3"></div>
        <div class="hero-shape shape-4"></div>
      </div>

      <!-- Subtle dot pattern overlay -->
      <div class="hero-pattern"></div>

      <div class="hero-content">
        <h1>
          <span class="hero-line-1">Discover Books</span>
          <span class="hero-line-2">You'll <em>Love</em></span>
        </h1>
        <p>Search, explore, purchase and download e-books across {{ catCount }} categories. Powered by smart recommendations tailored to your taste.</p>

        <div class="hero-stats">
          <div class="stat"><strong>{{ bookCount }}+</strong><span>Books</span></div>
          <div class="stat-divider"></div>
          <div class="stat"><strong>{{ catCount }}</strong><span>Categories</span></div>
        </div>

        <!-- Glass-morphism Search -->
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
          <el-button type="primary" size="large" class="btn-primary-hero" @click="$router.push('/books')">Browse Books</el-button>
          <el-button size="large" class="btn-outline-hero" @click="scrollToPopular">Popular Books</el-button>
        </div>
      </div>

      <!-- Scroll hint -->
      <div class="hero-scroll-hint" @click="scrollToDiscovery">
        <span>Explore the Store</span>
        <svg class="scroll-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="6 9 12 15 18 9"/>
        </svg>
      </div>

      <!-- Bottom fade transition -->
      <div class="hero-fade"></div>
    </section>

    <!-- Section 3: Smart Discovery -->
    <section class="section" id="discovery">
      <div class="section-head section-head-center">
        <h2>Smart Discovery</h2>
        <p class="section-subtitle">Discover books through multiple intelligent channels</p>
      </div>
      <div class="discovery-grid">
        <div class="discovery-card">
          <div class="discovery-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" class="discovery-svg">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
          </div>
          <h4>Search</h4>
          <p>Find any book instantly by title, author, or keyword across thousands of titles</p>
        </div>
        <div class="discovery-card">
          <div class="discovery-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" class="discovery-svg">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
          </div>
          <h4>Popular Ranking</h4>
          <p>Discover what others are reading — weighted by purchases, favorites, and views</p>
        </div>
        <div class="discovery-card">
          <div class="discovery-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" class="discovery-svg">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
            </svg>
          </div>
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
        <el-button text class="section-view-all" @click="$router.push('/hot')">
          View All
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="arrow-svg">
            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
          </svg>
        </el-button>
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
        <el-button text class="section-view-all" @click="$router.push('/recommended')">
          View All
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="arrow-svg">
            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
          </svg>
        </el-button>
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
   Pixel-Perfect · Modern · Refined Typography
   ══════════════════════════════════════════════════════════════ */

/* ── LandingNav Override: light-mode glassmorphism ── */
:deep(.landing-nav) {
  background: rgba(255,255,255,0.72) !important;
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border-bottom: 1px solid rgba(0,0,0,0.05);
}
:deep(.nav-brand)        { color: #0f172a !important; }
:deep(.logo-text)        { color: #0f172a !important; }
:deep(.nav-link)         { color: #475569 !important; }
:deep(.nav-link:hover)   { color: #2563eb !important; }
:deep(.nav-icon-btn)     { color: #475569 !important; background: transparent !important; }
:deep(.nav-icon-btn:hover) { color: #2563eb !important; background: rgba(37,99,235,0.06) !important; }
:deep(.nav-user-btn) {
  color: #1a1815 !important;
  background: rgba(37,99,235,0.04) !important;
  border: 1px solid #e5e5e5 !important;
}
:deep(.nav-user-btn:hover) {
  color: #2563eb !important;
  background: rgba(37,99,235,0.08) !important;
  border-color: #2563eb !important;
}
:deep(.nav-cta-btn) {
  color: #fff !important;
  background: #2563eb !important;
  box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
}
:deep(.nav-cta-btn:hover) {
  background: #1d4ed8 !important;
  box-shadow: 0 4px 14px rgba(37,99,235,0.4) !important;
}

/* ── Layout Reset ── */
.landing {
  width: 100%; min-height: 100vh; min-height: 100dvh;
  display: flex; flex-direction: column;
  overflow-x: hidden;
  background: #ffffff;
}

/* ══════════════════════════════════════════════════════════════
   Hero — "Depth & Light"
   Subtle blue-gray gradient base · bold floating geometry
   Glass search · scroll hint · pure white fade-out
   ══════════════════════════════════════════════════════════════ */
.hero {
  width: 100%; min-height: 100vh; min-height: 100dvh;
  display: flex; align-items: center; justify-content: center;
  /* Subtle blue-tinted gradient — like macOS System Settings */
  background:
    radial-gradient(ellipse 70% 55% at 50% 35%, rgba(219,234,254,0.40) 0%, transparent 55%),
    radial-gradient(ellipse 55% 45% at 85% 20%, rgba(224,231,255,0.30) 0%, transparent 50%),
    radial-gradient(ellipse 50% 40% at 15% 75%, rgba(236,240,255,0.30) 0%, transparent 55%),
    linear-gradient(180deg, #f8fafc 0%, #ffffff 30%, #fafafa 70%, #ffffff 100%);
  position: relative; overflow: hidden; isolation: isolate;
  flex-shrink: 0;
}

/* ── Floating geometric shapes ── */
.hero-shapes { position: absolute; inset: 0; pointer-events: none; z-index: 0; }
.hero-shape {
  position: absolute; border-radius: 50%;
  filter: blur(60px);
  animation: floatShape 18s ease-in-out infinite;
}
.shape-1 {
  width: 720px; height: 720px;
  top: -20%; right: -12%;
  background: radial-gradient(circle at 55% 45%,
    rgba(59,130,246,0.12) 0%,
    rgba(99,102,241,0.07) 30%,
    rgba(147,51,234,0.03) 60%,
    transparent 75%);
  animation-delay: 0s;
}
.shape-2 {
  width: 560px; height: 560px;
  bottom: -18%; left: -8%;
  background: radial-gradient(circle at 45% 55%,
    rgba(139,92,246,0.11) 0%,
    rgba(79,70,229,0.06) 35%,
    rgba(236,72,153,0.03) 60%,
    transparent 75%);
  animation-delay: -6s;
  animation-duration: 22s;
}
.shape-3 {
  width: 380px; height: 380px;
  top: 40%; right: 20%;
  background: radial-gradient(circle at 50% 50%,
    rgba(168,85,247,0.08) 0%,
    rgba(59,130,246,0.05) 45%,
    transparent 70%);
  animation-delay: -12s;
  animation-duration: 25s;
}
.shape-4 {
  width: 280px; height: 280px;
  bottom: 25%; left: 12%;
  background: radial-gradient(circle at 50% 50%,
    rgba(37,99,235,0.07) 0%,
    rgba(14,165,233,0.04) 50%,
    transparent 70%);
  animation-delay: -3s;
  animation-duration: 15s;
}
@keyframes floatShape {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(24px, -18px) scale(1.05); }
  50% { transform: translate(-14px, 12px) scale(0.97); }
  75% { transform: translate(-20px, -10px) scale(1.03); }
}

/* ── Dot pattern overlay ── */
.hero-pattern {
  position: absolute; inset: 0; z-index: 0; pointer-events: none;
  opacity: 0.18;
  background-image:
    radial-gradient(circle, rgba(0,0,0,0.06) 1px, transparent 1px);
  background-size: 24px 24px;
  mask-image: radial-gradient(ellipse 65% 55% at 50% 40%, black 25%, transparent 65%);
  -webkit-mask-image: radial-gradient(ellipse 65% 55% at 50% 40%, black 25%, transparent 65%);
}

/* ── Bottom Fade: smooth transition to first section ── */
.hero-fade {
  position: absolute; bottom: 0; left: 0; right: 0; z-index: 0;
  height: 140px;
  background: linear-gradient(to bottom, transparent, #ffffff);
  pointer-events: none;
}

/* ── Scroll Hint ── */
.hero-scroll-hint {
  position: absolute; bottom: 40px; left: 0; right: 0;
  margin: 0 auto; width: fit-content; z-index: 2;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  cursor: pointer; color: #94a3b8; user-select: none;
  transition: color 0.3s;
}
.hero-scroll-hint:hover { color: #2563eb; }
.hero-scroll-hint span {
  font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 500;
}
.scroll-chevron {
  width: 18px; height: 18px;
  animation: bounce 2s infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(5px); }
}

/* ── Content wrapper ── */
.hero-content {
  position: relative; z-index: 1;
  max-width: 860px; margin: 0 auto; padding: 120px 32px 80px;
  text-align: center; display: flex; flex-direction: column; align-items: center;
}

/* ═══ Zone 1 · Artistic Title ═══ */
.hero-content h1 {
  font-size: clamp(44px, 7vw, 80px);
  font-weight: 800;
  color: #0f172a;
  line-height: 1.06;
  letter-spacing: -2.4px;
  margin: 0 0 22px;
  display: flex; flex-direction: column; align-items: center; gap: 0;
}
.hero-line-1 {
  font-weight: 700;
  letter-spacing: -2px;
}
.hero-line-2 {
  font-weight: 900;
  letter-spacing: -2.8px;
}
.hero-line-2 em {
  font-style: normal;
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 35%, #7c3aed 65%, #3b82f6 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ═══ Zone 2 · Subtitle ═══ */
.hero-content > p {
  font-size: 17px; color: #64748b; max-width: 560px; margin: 0 0 48px;
  line-height: 1.7; font-weight: 400; letter-spacing: 0.1px;
}

/* ═══ Zone 3 · Stats ═══ */
.hero-stats {
  display: flex; align-items: center; gap: 36px;
  margin-bottom: 48px;
}
.stat { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.stat strong { font-size: 32px; font-weight: 700; color: #2563eb; letter-spacing: -0.6px; line-height: 1; }
.stat span  { font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.4px; font-weight: 500; }
.stat-divider {
  width: 1px; height: 36px;
  background: #e2e8f0;
  flex-shrink: 0;
}

/* ═══ Zone 4 · Glass-morphism Search ═══ */
.hero-search { width: min(560px, 88vw); margin-bottom: 22px; }
.hero-search-input :deep(.el-input__wrapper) {
  background: rgba(255,255,255,0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 14px; padding: 8px 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 4px 16px rgba(0,0,0,0.04);
  transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.hero-search-input :deep(.el-input__wrapper:hover) {
  border-color: rgba(0,0,0,0.14);
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.06);
}
.hero-search-input :deep(.el-input__wrapper.is-focus) {
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37,99,235,0.08), 0 4px 20px rgba(37,99,235,0.06);
  background: rgba(255,255,255,0.9);
}
.hero-search-input :deep(.el-input__inner) { color: #0f172a; font-size: 15px; }
.hero-search-input :deep(.el-input__inner::placeholder) { color: #94a3b8; }
.hero-search-input :deep(.el-input__prefix) { color: #94a3b8; }
.hero-search-input :deep(.el-input__clear) { color: #94a3b8; }

/* ═══ Zone 5 · CTAs ═══ */
.hero-actions {
  display: flex; gap: 14px; flex-wrap: wrap; justify-content: center;
}
.btn-primary-hero {
  font-weight: 600 !important; font-size: 16px !important;
  border-radius: 10px !important;
  padding: 14px 32px !important; height: auto !important;
  background: #2563eb !important; border: none !important;
  box-shadow: 0 4px 14px rgba(37,99,235,0.28) !important;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
  letter-spacing: 0.2px !important;
}
.btn-primary-hero:hover {
  background: #1d4ed8 !important;
  box-shadow: 0 6px 20px rgba(37,99,235,0.36) !important;
  transform: translateY(-1px);
}
.btn-outline-hero {
  font-weight: 600 !important; font-size: 16px !important;
  border-radius: 10px !important;
  padding: 14px 32px !important; height: auto !important;
  background: transparent !important;
  border: 1.5px solid #cbd5e1 !important;
  color: #334155 !important;
  letter-spacing: 0.2px !important;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
}
.btn-outline-hero:hover {
  border-color: #2563eb !important;
  color: #2563eb !important;
  background: rgba(37,99,235,0.03) !important;
  box-shadow: 0 4px 14px rgba(37,99,235,0.08) !important;
  transform: translateY(-1px);
}

/* ══════════════════════════════════════════════════════════════
   Sections — Warm Alternating Rhythm
   ══════════════════════════════════════════════════════════════ */
.section {
  max-width: 1280px; margin: 0 auto; padding: 96px 28px;
}
.section-alt {
  background: transparent; max-width: none;
}
/* No borders — cards provide natural separation */
.section-alt > * { max-width: 1280px; margin-left: auto; margin-right: auto; }
.section-head {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 32px;
}
.section-head h2 {
  font-size: 34px; font-weight: 700; color: #0f172a; margin: 0 0 4px;
  letter-spacing: -0.6px;
}
.section-head-center { text-align: center; flex-direction: column; }
.section-subtitle { font-size: 15px; color: #8b7e74; margin: 0; line-height: 1.5; }
.section-view-all {
  font-size: 15px !important; font-weight: 500 !important;
  color: #2563eb !important;
  display: flex !important; align-items: center !important; gap: 4px !important;
  transition: gap 0.25s ease !important;
}
.section-view-all:hover { gap: 8px !important; }
.arrow-svg { width: 16px; height: 16px; }

/* ══════════════════════════════════════════════════════════════
   Smart Discovery Cards — Warm & Airy
   ══════════════════════════════════════════════════════════════ */
.discovery-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.discovery-card {
  background: #ffffff;
  border: 1px solid #f0f0f0;
  border-radius: 18px;
  padding: 40px 32px; text-align: center;
  box-shadow: 0 1px 2px rgba(0,0,0,0.02);
  transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.discovery-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.05), 0 3px 8px rgba(0,0,0,0.025);
  border-color: #e0e0e0;
}
.discovery-icon {
  width: 68px; height: 68px; border-radius: 18px;
  background: rgba(37,99,235,0.06); color: #2563eb;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 18px;
}
.discovery-svg { width: 32px; height: 32px; display: block; }
.discovery-card h4 { font-size: 18px; font-weight: 600; color: #1a1815; margin: 0 0 8px; }
.discovery-card p  { font-size: 14px; color: #8b7e74; line-height: 1.65; margin: 0; }

/* ══════════════════════════════════════════════════════════════
   Book Cards — Warm White · Soft Elevation
   ══════════════════════════════════════════════════════════════ */
.book-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}
.book-card {
  cursor: pointer; border-radius: 10px;
  background: #ffffff; border: none;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.10);
}
.book-card img {
  width: 100%; aspect-ratio: 2/3; object-fit: cover; display: block;
  background: #ffffff;
}
.book-card-info { padding: 18px 16px; }
.book-card-info h4 {
  font-size: 14px; font-weight: 600; color: #1e1b18;
  margin: 0 0 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  line-height: 1.3;
}
.book-author { font-size: 13px; color: #a0968c; display: block; margin-bottom: 10px; }
.book-price { font-size: 16px; font-weight: 700; color: #1a1815; }

/* ══════════════════════════════════════════════════════════════
   Footer — Warm Deep Tone
   ══════════════════════════════════════════════════════════════ */
.landing-footer { margin-top: auto; background: #1d1a1c; color: #bfb8b0; padding: 64px 28px 36px; }
.footer-inner { max-width: 1280px; margin: 0 auto; display: flex; gap: 72px; flex-wrap: wrap; margin-bottom: 44px; }
.footer-brand { max-width: 340px; }
.footer-brand h3 { color: #f3efe8; font-size: 20px; font-weight: 700; margin: 0 0 10px; letter-spacing: 0.2px; }
.footer-brand p { color: #a0988c; font-size: 14px; line-height: 1.65; margin: 0; }
.footer-links { display: flex; gap: 72px; }
.footer-col h4 { color: #f3efe8; font-size: 13px; font-weight: 600; margin: 0 0 14px; text-transform: uppercase; letter-spacing: 0.8px; }
.footer-col a { display: block; color: #a0988c; font-size: 14px; margin-bottom: 10px; transition: color 0.2s; }
.footer-col a:hover { color: #f3efe8; }
.footer-bottom { max-width: 1280px; margin: 0 auto; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.06); text-align: center; }
.footer-bottom p { color: #7a7268; font-size: 13px; margin: 0; }

/* ══════════════════════════════════════════════════════════════
   Responsive
   ══════════════════════════════════════════════════════════════ */
@media (max-width: 1024px) {
  .book-grid { grid-template-columns: repeat(3, 1fr); gap: 20px; }
}
@media (max-width: 768px) {
  .discovery-grid { grid-template-columns: repeat(1, 1fr); gap: 16px; }
  .book-grid { grid-template-columns: repeat(2, 1fr); gap: 16px; }
  .hero-content { padding: 104px 24px 72px; }
  .hero-content h1 { font-size: clamp(36px, 8vw, 56px); letter-spacing: -1.8px; margin-bottom: 16px; }
  .hero-content > p { margin-bottom: 40px; }
  .hero-stats { margin-bottom: 40px; gap: 28px; }
  .hero-shape { opacity: 0.4; }
  .hero-pattern { opacity: 0.14; }
  .section { padding: 64px 20px; }
}
@media (max-width: 640px) {
  .hero-content { padding: 92px 20px 60px; }
  .hero-content h1 { font-size: clamp(30px, 9vw, 44px); letter-spacing: -1.5px; margin-bottom: 14px; }
  .hero-line-2 { letter-spacing: -1.8px; }
  .hero-content > p { font-size: 15px; margin-bottom: 34px; max-width: 100%; }
  .hero-stats { gap: 22px; margin-bottom: 34px; }
  .stat strong { font-size: 26px; }
  .hero-search { width: 100%; margin-bottom: 18px; }
  .hero-shape { opacity: 0.7; }
  .hero-pattern { opacity: 0.10; }
  .hero-scroll-hint { bottom: 28px; }
  .hero-scroll-hint span { font-size: 10px; }
  .footer-inner { flex-direction: column; gap: 36px; }
  .footer-links { gap: 36px; }
}
</style>
