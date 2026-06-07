<template>
  <nav class="landing-nav">
    <div class="nav-inner">
      <router-link to="/" class="nav-brand">EBookStore</router-link>

      <!-- Main nav links -->
      <div class="nav-links">
        <router-link to="/" class="nav-item" exact-active-class="nav-item--active">Home</router-link>
        <router-link to="/books" class="nav-item" active-class="nav-item--active">Browse</router-link>
        <router-link to="/recommended" class="nav-item" active-class="nav-item--active">Recommend</router-link>
        <router-link to="/hot" class="nav-item" active-class="nav-item--active">Popular</router-link>
      </div>

      <div class="nav-spacer"></div>
      <template v-if="auth.isLoggedIn">
        <!-- Favorites icon — modern minimalist heart SVG -->
        <el-button class="nav-icon-btn" @click="$router.push('/favorites')" title="Favorites">
          <svg class="nav-svg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
        </el-button>
        <!-- Cart icon — modern minimalist bag SVG -->
        <el-badge :value="cart.count" :hidden="!cart.count" class="nav-cart">
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
        <el-button text class="nav-link" @click="$router.push('/login')">Sign In</el-button>
        <el-button class="nav-cta-btn" @click="$router.push('/register')">Get Started</el-button>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useCartStore } from '../store/cart'

const router = useRouter()
const auth = useAuthStore()
const cart = useCartStore()

if (auth.isLoggedIn) cart.fetch()

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
/* ══════════════════════════════════════════════════════════════
   LandingNav — Refined Modern Navigation
   Clean typography, unified sizing, minimalist icons
   ══════════════════════════════════════════════════════════════ */

.landing-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  padding: 0 28px;
  background: transparent;
  transition: background 0.3s ease;
}

.nav-inner {
  display: flex; align-items: center; height: 68px;
  max-width: 1320px; margin: 0 auto; gap: 20px;
}

/* ── Brand — unified size with nav items ── */
.nav-brand {
  font-size: 15px; font-weight: 600; color: #fff;
  letter-spacing: 0.3px;
  flex-shrink: 0;
  transition: opacity 0.2s;
}
.nav-brand:hover { opacity: 0.85; }

/* ── Nav Links — unified typography ── */
.nav-links {
  display: flex; align-items: center; gap: 4px;
  margin-left: 32px;
}
.nav-item {
  font-size: 15px; font-weight: 500; color: rgba(255,255,255,0.72);
  padding: 8px 16px; border-radius: 10px;
  letter-spacing: 0.2px;
  transition: all 0.25s ease;
}
.nav-item:hover { color: #fff; background: rgba(255,255,255,0.08); }
.nav-item--active { color: #fff; background: rgba(255,255,255,0.12); font-weight: 600; }

.nav-spacer { flex: 1; }

/* ── Sign In link — unified typography ── */
.nav-link {
  font-size: 15px !important; font-weight: 500 !important;
  color: rgba(255,255,255,0.82) !important;
  letter-spacing: 0.2px !important;
  padding: 8px 16px !important;
}
.nav-link:hover { color: #fff !important; }

/* ── Get Started CTA — unified typography ── */
.nav-cta-btn {
  font-size: 15px !important; font-weight: 600 !important;
  letter-spacing: 0.2px !important;
  color: #fff !important;
  background: #2563eb !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 9px 22px !important;
  height: auto !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
}
.nav-cta-btn:hover {
  background: #1d4ed8 !important;
  box-shadow: 0 4px 14px rgba(37,99,235,0.4) !important;
  transform: translateY(-1px);
}

/* ── Icon Buttons — consistent sizing ── */
.nav-icon-btn {
  width: 40px !important; height: 40px !important;
  padding: 0 !important;
  color: rgba(255,255,255,0.75) !important;
  background: transparent !important;
  border: none !important;
  border-radius: 10px !important;
  display: flex !important; align-items: center !important; justify-content: center !important;
  transition: all 0.25s ease !important;
}
.nav-icon-btn:hover {
  color: #fff !important;
  background: rgba(255,255,255,0.1) !important;
}

/* ── Custom SVG Icons ── */
.nav-svg-icon {
  width: 20px; height: 20px;
  display: block;
}
.nav-svg-chevron {
  width: 14px; height: 14px;
  margin-left: 2px;
}

.nav-cart { margin-right: 4px; }

/* ── User Dropdown Button — unified typography ── */
.nav-user-btn {
  font-size: 15px !important; font-weight: 500 !important;
  letter-spacing: 0.2px !important;
  background: rgba(255,255,255,0.12) !important;
  border: 1px solid rgba(255,255,255,0.2) !important;
  color: #fff !important;
  border-radius: 10px !important;
  padding: 8px 16px !important;
  height: auto !important;
  display: flex !important; align-items: center !important; gap: 4px !important;
  transition: all 0.25s ease !important;
}
.nav-user-btn:hover {
  background: rgba(255,255,255,0.18) !important;
  border-color: rgba(255,255,255,0.3) !important;
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .landing-nav { padding: 0 16px; }
  .nav-links { display: none; }
  .nav-inner { gap: 12px; }
}
</style>
