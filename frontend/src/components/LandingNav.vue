<template>
  <nav class="landing-nav">
    <div class="nav-inner">
      <router-link to="/" class="nav-brand">EBookStore</router-link>
      <div class="nav-spacer"></div>
      <template v-if="auth.isLoggedIn">
        <el-badge :value="cart.count" :hidden="!cart.count" class="nav-cart">
          <el-button icon="ShoppingCart" circle text @click="$router.push('/cart')" class="nav-icon-btn" />
        </el-badge>
        <el-dropdown>
          <el-button class="nav-user-btn">
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
        <el-button text class="nav-link" @click="$router.push('/login')">Sign In</el-button>
        <el-button type="primary" size="small" round @click="$router.push('/register')">Get Started</el-button>
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
.landing-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  padding: 0 24px;
  background: transparent;
  transition: background 0.3s;
}
.nav-inner {
  display: flex; align-items: center; height: 64px;
  max-width: 1280px; margin: 0 auto; gap: 16px;
}
.nav-brand {
  font-size: 22px; font-weight: 700; color: #fff;
  letter-spacing: -0.5px;
}
.nav-spacer { flex: 1; }
.nav-link { color: rgba(255,255,255,0.85) !important; }
.nav-link:hover { color: #fff !important; }
.nav-icon-btn { color: rgba(255,255,255,0.75) !important; }
.nav-icon-btn:hover { color: #fff !important; }
.nav-cart { margin-right: 4px; }
.nav-user-btn {
  background: rgba(255,255,255,0.12) !important;
  border: 1px solid rgba(255,255,255,0.2) !important;
  color: #fff !important;
}
.nav-user-btn:hover {
  background: rgba(255,255,255,0.18) !important;
}
</style>
