<template>
  <div class="main-layout">
    <el-container>
      <el-header class="header">
        <div class="header-inner">
          <!-- Hamburger — mobile only -->
          <button class="hamburger-btn" @click="mobileOpen = true" aria-label="Menu">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>

          <div class="logo">
            <router-link to="/">
              <svg class="logo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              <span class="logo-text">EBook Store</span>
            </router-link>
          </div>

          <div class="header-search">
            <el-input
              v-model="searchQuery"
              placeholder="Search books..."
              prefix-icon="Search"
              clearable
              @keyup.enter="doSearch"
              @clear="searchQuery = ''"
            />
          </div>

          <div class="header-nav">
            <div class="nav-links">
              <router-link to="/" class="nav-item" exact-active-class="nav-item--active">Home</router-link>
              <router-link to="/books" class="nav-item" active-class="nav-item--active">Browse</router-link>
              <router-link to="/recommended" class="nav-item" active-class="nav-item--active">Recommend</router-link>
              <router-link to="/hot" class="nav-item" active-class="nav-item--active">Popular</router-link>
            </div>

            <div class="header-actions">
              <template v-if="auth.isLoggedIn">
                <el-button class="nav-icon-btn" @click="$router.push('/favorites')" title="Favorites">
                  <svg class="nav-svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                  </svg>
                </el-button>
                <el-badge :value="cart.count" :hidden="cart.count === 0" class="cart-badge">
                  <el-button class="nav-icon-btn" @click="$router.push('/cart')" title="Cart">
                    <svg class="nav-svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
                      <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
                    </svg>
                  </el-button>
                </el-badge>
                <el-dropdown>
                  <el-button class="nav-user-btn">
                    {{ auth.user?.username }}
                    <svg class="nav-svg-icon nav-svg-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="6 9 12 15 18 9"/>
                    </svg>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="$router.push('/profile')">Profile</el-dropdown-item>
                      <el-dropdown-item @click="$router.push('/favorites')">Favorites</el-dropdown-item>
                      <el-dropdown-item @click="$router.push('/orders')">Orders</el-dropdown-item>
                      <el-dropdown-item @click="$router.push('/downloads')">Downloads</el-dropdown-item>
                      <el-dropdown-item v-if="auth.isAdmin" @click="$router.push('/admin')" divided>Admin Panel</el-dropdown-item>
                      <el-dropdown-item @click="handleLogout" divided>Logout</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </template>
              <template v-else>
                <el-button class="nav-signin-btn" @click="$router.push('/login')">Sign In</el-button>
                <el-button type="primary" class="nav-cta-btn" @click="$router.push('/register')">Get Started</el-button>
              </template>
            </div>
          </div>
        </div>
      </el-header>

      <!-- Mobile navigation drawer -->
      <el-drawer v-model="mobileOpen" direction="left" size="280px" :with-header="false">
        <div class="mobile-nav">
          <div class="mobile-nav-brand">EBook Store</div>
          <router-link to="/" class="mobile-nav-item" @click="mobileOpen = false">Home</router-link>
          <router-link to="/books" class="mobile-nav-item" @click="mobileOpen = false">Browse</router-link>
          <router-link to="/recommended" class="mobile-nav-item" @click="mobileOpen = false">Recommend</router-link>
          <router-link to="/hot" class="mobile-nav-item" @click="mobileOpen = false">Popular</router-link>
          <el-divider />
          <router-link to="/profile" class="mobile-nav-item" @click="mobileOpen = false" v-if="auth.isLoggedIn">Profile</router-link>
          <router-link to="/favorites" class="mobile-nav-item" @click="mobileOpen = false" v-if="auth.isLoggedIn">Favorites</router-link>
          <router-link to="/orders" class="mobile-nav-item" @click="mobileOpen = false" v-if="auth.isLoggedIn">Orders</router-link>
          <router-link to="/downloads" class="mobile-nav-item" @click="mobileOpen = false" v-if="auth.isLoggedIn">Downloads</router-link>
          <router-link to="/admin" class="mobile-nav-item" @click="mobileOpen = false" v-if="auth.isAdmin">Admin Panel</router-link>
          <el-divider />
          <router-link to="/login" class="mobile-nav-item" @click="mobileOpen = false" v-if="!auth.isLoggedIn">Sign In</router-link>
          <router-link to="/register" class="mobile-nav-item mobile-nav-cta" @click="mobileOpen = false" v-if="!auth.isLoggedIn">Get Started</router-link>
          <a class="mobile-nav-item mobile-nav-logout" @click="handleLogout" v-if="auth.isLoggedIn">Logout</a>
        </div>
      </el-drawer>

      <el-main class="main-content">
        <router-view />
      </el-main>

      <el-footer class="footer">
        <p>&copy; 2026 EBook Store. All rights reserved. Built with Vue 3 & Django.</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useCartStore } from '../store/cart'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const cart = useCartStore()

const searchQuery = ref('')
const mobileOpen = ref(false)

if (auth.isLoggedIn) cart.fetch()

watch(() => route.path, () => {
  if (auth.isLoggedIn) cart.fetch()
})

function doSearch() {
  if (searchQuery.value.trim()) {
    router.push({ name: 'Search', query: { q: searchQuery.value.trim() } })
  }
}

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
/* ══════════════════════════════════════════════════════════════
   MainLayout — Unified Design Language
   Clean, modern, pixel-perfect with custom SVG icons
   ══════════════════════════════════════════════════════════════ */

.main-layout { min-height: 100vh; background: #ffffff; display: flex; flex-direction: column; }
.main-layout :deep(.el-container) { flex: 1; display: flex; flex-direction: column; }

.header {
  background: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  padding: 0 24px;
  position: sticky; top: 0; z-index: 100;
}

.header-inner {
  display: flex; align-items: center; height: 64px;
  gap: 24px; max-width: 1400px; margin: 0 auto;
}

/* ── Logo ── */
.logo a { display: flex; align-items: center; gap: 10px; color: #2563eb; }
.logo-icon { width: 26px; height: 26px; }
.logo-text { font-size: 18px; font-weight: 700; letter-spacing: -0.3px; color: #0f172a; }

/* ── Search ── */
.header-search { flex: 1; max-width: 480px; }

/* ── Nav Links — custom, no overflow/ellipsis ── */
.header-nav { display: flex; align-items: center; gap: 16px; margin-left: auto; }

.nav-links { display: flex; align-items: center; gap: 4px; }
.nav-item {
  font-size: 15px; font-weight: 500; color: #6b5e54;
  padding: 8px 16px; border-radius: 10px;
  letter-spacing: 0.2px;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.nav-item:hover { color: #2563eb; background: rgba(37,99,235,0.05); }
.nav-item--active { color: #2563eb; background: rgba(37,99,235,0.08); font-weight: 600; }

.header-actions { display: flex; align-items: center; gap: 8px; }

/* ── Icon Buttons ── */
.nav-icon-btn {
  width: 40px !important; height: 40px !important;
  padding: 0 !important;
  color: #475569 !important;
  background: transparent !important;
  border: none !important;
  border-radius: 10px !important;
  display: flex !important; align-items: center !important; justify-content: center !important;
  transition: all 0.2s ease !important;
}
.nav-icon-btn:hover {
  color: #2563eb !important;
  background: rgba(37,99,235,0.06) !important;
}
.nav-svg-icon { width: 20px; height: 20px; display: block; }
.nav-svg-chevron { width: 14px; height: 14px; margin-left: 2px; }

.cart-badge { margin-right: 4px; }

/* ── Sign In / CTA Buttons ── */
.nav-signin-btn {
  font-size: 14px !important; font-weight: 500 !important;
  color: #6b5e54 !important;
  border: none !important;
  background: transparent !important;
  padding: 8px 16px !important;
  border-radius: 10px !important;
  transition: all 0.2s ease !important;
}
.nav-signin-btn:hover {
  color: #2563eb !important;
  background: rgba(37,99,235,0.05) !important;
}

.nav-cta-btn {
  font-size: 14px !important; font-weight: 600 !important;
  background: #2563eb !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 8px 20px !important;
  box-shadow: 0 2px 6px rgba(37,99,235,0.25) !important;
  transition: all 0.2s ease !important;
}
.nav-cta-btn:hover {
  background: #1d4ed8 !important;
  box-shadow: 0 4px 12px rgba(37,99,235,0.35) !important;
}

/* ── User Dropdown ── */
.nav-user-btn {
  font-size: 14px !important; font-weight: 500 !important;
  color: #1a1815 !important;
  background: #ffffff !important;
  border: 1px solid #e5e5e5 !important;
  border-radius: 10px !important;
  padding: 8px 16px !important;
  display: flex !important; align-items: center !important; gap: 4px !important;
  transition: all 0.2s ease !important;
}
.nav-user-btn:hover {
  border-color: #2563eb !important;
  color: #2563eb !important;
  background: rgba(37,99,235,0.04) !important;
}

/* ── Main Content ── */
.main-content {
  max-width: 1400px; margin: 0 auto; padding: 24px; width: 100%;
  flex: 1;
}

/* ── Footer ── */
.footer {
  text-align: center; padding: 20px;
  background: #ffffff; color: #a0988c; font-size: 13px;
  border-top: 1px solid #f0f0f0;
}

/* ── Hamburger — hidden on desktop ── */
.hamburger-btn { display: none; }

/* ═══════════════════════════════════════════════════════
   Mobile — below 768px
   ═══════════════════════════════════════════════════════ */
@media (max-width: 768px) {
  /* Hamburger button */
  .hamburger-btn {
    display: flex;
    align-items: center; justify-content: center;
    width: 40px; height: 40px; padding: 0;
    border: none; border-radius: 10px;
    background: transparent; color: #475569; cursor: pointer;
    flex-shrink: 0;
  }
  .hamburger-btn svg { width: 22px; height: 22px; }

  .header { padding: 0 12px; }
  .header-inner { gap: 8px; height: 56px; }

  .logo-text { font-size: 15px; }
  .logo-icon { width: 22px; height: 22px; }

  /* Hide desktop nav */
  .header-nav { display: none; }
  /* Search takes remaining space */
  .header-search { flex: 1; max-width: none; }

  .main-content { padding: 16px; }

  .footer { padding: 16px; font-size: 12px; }
}

/* Mobile nav drawer */
.mobile-nav {
  display: flex; flex-direction: column; padding: 24px 0;
}
.mobile-nav-brand {
  font-size: 20px; font-weight: 700; color: #2563eb;
  letter-spacing: -0.3px; padding: 0 24px; margin-bottom: 20px;
}
.mobile-nav-item {
  display: block; padding: 12px 24px; font-size: 15px; font-weight: 500;
  color: #334155; text-decoration: none; transition: background 0.15s;
}
.mobile-nav-item:hover { background: rgba(37,99,235,0.04); color: #2563eb; }
.mobile-nav-cta {
  color: #2563eb; font-weight: 600;
}
.mobile-nav-logout {
  color: #94a3b8; cursor: pointer;
}
</style>
