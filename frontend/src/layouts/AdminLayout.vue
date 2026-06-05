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
  background: #304156;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
}

.admin-logo {
  padding: 20px 16px;
  text-align: center;
  flex-shrink: 0;
}

.admin-logo a {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.admin-menu {
  flex: 1;
  border-right: none !important;
  overflow-y: auto;
}

.admin-menu .el-menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.admin-sidebar-footer {
  padding: 16px;
  text-align: center;
  flex-shrink: 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-right {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.admin-header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  height: 56px;
  flex-shrink: 0;
}

.admin-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.admin-header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-user {
  color: #666;
  font-size: 14px;
}

.admin-main {
  background: #f0f2f5;
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}
</style>
