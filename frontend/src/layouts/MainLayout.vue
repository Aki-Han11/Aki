<template>
  <div class="main-layout">
    <el-container>
      <el-header class="header" :class="{ 'header-transparent': isHome }">
        <div class="header-inner">
          <div class="logo">
            <router-link to="/">
              <el-icon :size="28"><Reading /></el-icon>
              <span class="logo-text" :class="{ 'logo-text-light': isHome }">EBook Store</span>
            </router-link>
          </div>

          <div class="header-search" v-show="!isHome">
            <el-input
              v-model="searchQuery"
              placeholder="Search books by title, author or tags..."
              prefix-icon="Search"
              clearable
              @keyup.enter="doSearch"
              @clear="searchQuery = ''"
            />
          </div>

          <div class="header-nav">
            <el-menu v-show="!isHome" mode="horizontal" :router="true" :default-active="activeMenu" class="nav-menu">
              <el-menu-item index="/">Home</el-menu-item>
              <el-menu-item index="/books">Browse</el-menu-item>
            </el-menu>

            <div class="header-actions">
              <template v-if="auth.isLoggedIn">
                <el-badge :value="cart.count" :hidden="cart.count === 0" class="cart-badge">
                  <el-button icon="ShoppingCart" circle @click="$router.push('/cart')" />
                </el-badge>
                <el-dropdown>
                  <el-button type="primary" plain>
                    {{ auth.user?.username }}
                    <el-icon class="el-icon--right"><ArrowDown /></el-icon>
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
                <el-button class="header-login-btn" :class="{ 'btn-light': isHome }" @click="$router.push('/login')">Sign In</el-button>
                <el-button type="primary" @click="$router.push('/register')">Get Started</el-button>
              </template>
            </div>
          </div>
        </div>
      </el-header>

      <el-main class="main-content" :class="{ 'no-padding': isHome }">
        <router-view />
      </el-main>

      <el-footer class="footer">
        <p>&copy; 2026 EBook Store. All rights reserved. Built with Vue 3 & Django.</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useCartStore } from '../store/cart'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const cart = useCartStore()

const searchQuery = ref('')
const isHome = computed(() => route.path === '/')

const activeMenu = computed(() => {
  if (route.path === '/' || route.path.startsWith('/books')) return route.path
  return '/'
})

if (auth.isLoggedIn) {
  cart.fetch()
}

// Refresh cart count on every navigation
watch(() => route.path, () => {
  if (auth.isLoggedIn) {
    cart.fetch()
  }
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
.main-layout { min-height: 100vh; }

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 0 20px;
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background 0.3s, box-shadow 0.3s;
}

/* Transparent mode on homepage */
.header-transparent {
  position: absolute;
  top: 0; left: 0; right: 0;
  background: transparent;
  box-shadow: none;
  z-index: 10;
}

.header-inner {
  display: flex; align-items: center; height: 64px;
  gap: 20px; max-width: 1400px; margin: 0 auto;
}

.logo a { display: flex; align-items: center; gap: 8px; color: #409eff; }
.logo-text { font-size: 22px; font-weight: 700; letter-spacing: -1px; }
.logo-text-light { color: #fff; }

.header-search { flex: 1; max-width: 500px; }

.header-nav { display: flex; align-items: center; gap: 12px; margin-left: auto; }
.nav-menu { border-bottom: none !important; }
.header-actions { display: flex; align-items: center; gap: 10px; }
.cart-badge { margin-right: 4px; }

.btn-light {
  color: rgba(255,255,255,0.85) !important;
  border-color: rgba(255,255,255,0.3) !important;
}
.btn-light:hover { color: #fff !important; border-color: rgba(255,255,255,0.6) !important; }

.main-content {
  max-width: 1400px; margin: 0 auto; padding: 20px;
  min-height: calc(100vh - 124px);
}
.main-content.no-padding {
  padding: 0; max-width: none;
}

.footer {
  text-align: center; padding: 20px;
  background: #fff; color: #999; font-size: 14px;
}
</style>
