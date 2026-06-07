<template>
  <div class="admin-layout">
    <el-container class="admin-container">
      <el-aside width="220px" class="admin-sidebar">
        <div class="admin-logo">
          <router-link to="/admin">
            <el-icon :size="24"><Setting /></el-icon>
            <span>Admin Panel</span>
          </router-link>
        </div>
        <el-menu
          :router="true"
          :default-active="activeMenu"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409eff"
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
          <el-button type="info" plain size="small" @click="$router.push('/')">
            <el-icon><Back /></el-icon> Back to Store
          </el-button>
        </div>
      </el-aside>

      <el-container class="admin-right">
        <el-header class="admin-header">
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
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const activeMenu = computed(() => route.path)

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
  background: #1e293b;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
}

.admin-logo {
  padding: 22px 20px;
  flex-shrink: 0;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.admin-logo a {
  color: #fff;
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
}
.admin-menu :deep(.el-menu-item.is-active) { background: rgba(64,158,255,0.15) !important; }

.admin-sidebar-footer {
  padding: 16px; text-align: center; flex-shrink: 0;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.admin-right {
  display: flex; flex-direction: column; overflow: hidden;
}

.admin-header {
  background: #fff;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); height: 56px; flex-shrink: 0;
}

.admin-title {
  font-size: 17px; font-weight: 600; color: #1e293b; letter-spacing: -0.2px;
}

.admin-header-right {
  display: flex; align-items: center; gap: 14px;
}

.admin-user {
  color: #64748b; font-size: 13px; font-weight: 500;
}

.admin-main {
  background: #f8fafc; flex: 1; overflow-y: auto; padding: 24px 28px;
}
</style>
