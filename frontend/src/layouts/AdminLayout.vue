<template>
  <div class="admin-layout">
    <el-container class="admin-container">
      <div class="admin-sidebar-overlay" :class="{ open: sidebarOpen }" @click="sidebarOpen = false"></div>
      <el-aside width="220px" class="admin-sidebar" :class="{ 'sidebar-open': sidebarOpen }">
        <div class="admin-logo">
          <router-link to="/admin">
            <el-icon :size="24"><Setting /></el-icon>
            <span>Admin Panel</span>
          </router-link>
        </div>
        <el-menu
          :router="true"
          :default-active="activeMenu"
          background-color="#ffffff"
          text-color="#475569"
          active-text-color="#2563eb"
          class="admin-menu"
        >
          <el-menu-item index="/admin">
            <el-icon><DataAnalysis /></el-icon>
            <span>Dashboard</span>
          </el-menu-item>
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <span>Users</span>
          </el-menu-item>
          <el-menu-item index="/admin/books">
            <el-icon><Document /></el-icon>
            <span>Books</span>
          </el-menu-item>
          <el-menu-item index="/admin/categories">
            <el-icon><Collection /></el-icon>
            <span>Categories</span>
          </el-menu-item>
          <el-menu-item index="/admin/recommendations">
            <el-icon><MagicStick /></el-icon>
            <span>Recommendations</span>
          </el-menu-item>
        </el-menu>
        <div class="admin-sidebar-footer">
          <el-button class="back-btn" @click="$router.push('/')">Back to Store</el-button>
        </div>
      </el-aside>

      <el-container class="admin-right">
        <el-header class="admin-header">
          <button class="admin-menu-toggle" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle menu">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>
          <span class="admin-title">{{ pageTitle }}</span>
          <div class="admin-header-right">
            <span class="admin-user">{{ auth.user?.username }}</span>
            <el-button size="small" @click="handleLogout">Logout</el-button>
          </div>
        </el-header>
        <el-main class="admin-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const activeMenu = computed(() => route.path)
const sidebarOpen = ref(false)

const pageTitle = computed(() => {
  const titles = {
    '/admin': 'Dashboard',
    '/admin/users': 'User Management',
    '/admin/books': 'Book Management',
    '/admin/categories': 'Category Management',
    '/admin/recommendations': 'Recommendation Management',
  }
  return titles[route.path] || 'Admin Panel'
})

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  overflow: hidden;
}

.admin-container {
  height: 100%;
}

.admin-sidebar {
  background: #ffffff;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
  border-right: 1px solid #f0f0f0;
}

.admin-logo {
  padding: 22px 20px;
  flex-shrink: 0;
  border-bottom: 1px solid #f0f0f0;
}

.admin-logo a {
  color: #2563eb;
  font-size: 17px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
  letter-spacing: -0.3px;
}

.admin-menu {
  flex: 1;
  border-right: none !important;
  overflow-y: auto;
  padding: 8px 0;
}

.admin-menu :deep(.el-menu-item) {
  margin: 2px 8px; border-radius: 8px; height: 42px; line-height: 42px;
  color: #475569;
}
.admin-menu :deep(.el-menu-item:hover) { background: rgba(37,99,235,0.04) !important; }
.admin-menu :deep(.el-menu-item.is-active) {
  background: rgba(37,99,235,0.08) !important;
  color: #2563eb !important;
  font-weight: 600;
}

.admin-sidebar-footer {
  padding: 16px; text-align: center; flex-shrink: 0;
  border-top: 1px solid #f0f0f0;
}

/* Back to Store button */
.back-btn {
  background: transparent !important;
  border: 1px solid #e5e5e5 !important;
  color: #475569 !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  border-radius: 8px !important;
  padding: 8px 20px !important;
  transition: all 0.2s ease !important;
}
.back-btn:hover {
  border-color: #2563eb !important;
  color: #2563eb !important;
  background: rgba(37,99,235,0.04) !important;
}

.admin-right {
  display: flex; flex-direction: column; overflow: hidden;
}

.admin-header {
  background: #ffffff;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); height: 56px; flex-shrink: 0;
}

.admin-title {
  font-size: 17px; font-weight: 600; color: #1a1815; letter-spacing: -0.2px;
}

.admin-header-right {
  display: flex; align-items: center; gap: 14px;
}

.admin-user {
  color: #8b7e74; font-size: 13px; font-weight: 500;
}

.admin-main {
  background: #ffffff; flex: 1; overflow-y: auto; padding: 24px 28px 48px;
}

/* ═══════════════════════════════════════════════════════
   Mobile — below 768px
   ═══════════════════════════════════════════════════════ */
@media (max-width: 768px) {
  /* Sidebar becomes overlay */
  .admin-sidebar {
    position: fixed; top: 0; left: 0; bottom: 0; z-index: 200;
    width: 260px; transform: translateX(-100%);
    transition: transform 0.25s ease;
    box-shadow: 4px 0 20px rgba(0,0,0,0.08);
  }
  .admin-sidebar.sidebar-open { transform: translateX(0); }

  /* Overlay backdrop */
  .admin-sidebar-overlay {
    display: none;
    position: fixed; inset: 0; z-index: 199;
    background: rgba(0,0,0,0.3);
  }
  .admin-sidebar-overlay.open { display: block; }

  /* Toggle button */
  .admin-menu-toggle {
    display: flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; padding: 0; margin-right: 8px;
    border: none; border-radius: 8px; flex-shrink: 0;
    background: transparent; color: #475569; cursor: pointer;
  }
  .admin-menu-toggle svg { width: 20px; height: 20px; }

  .admin-header { padding: 0 16px; }
  .admin-main { padding: 16px; }
  .admin-user { display: none; }
}
</style>
