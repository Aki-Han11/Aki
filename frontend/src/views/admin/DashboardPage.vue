<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stat-cards">
      <el-col :xs="12" :sm="6" class="stat-col">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-inner">
            <div class="stat-icon users">
              <el-icon :size="28"><User /></el-icon>
            </div>
            <div class="stat-body">
              <div class="stat-value">{{ stats.total_users || 0 }}</div>
              <div class="stat-label">Total Users</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6" class="stat-col">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-inner">
            <div class="stat-icon books">
              <el-icon :size="28"><Document /></el-icon>
            </div>
            <div class="stat-body">
              <div class="stat-value">{{ stats.total_books || 0 }}</div>
              <div class="stat-label">Total Books</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6" class="stat-col">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-inner">
            <div class="stat-icon orders">
              <el-icon :size="28"><ShoppingCart /></el-icon>
            </div>
            <div class="stat-body">
              <div class="stat-value">{{ stats.total_orders || 0 }}</div>
              <div class="stat-label">Total Orders</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6" class="stat-col">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-inner">
            <div class="stat-icon revenue">
              <el-icon :size="28"><Money /></el-icon>
            </div>
            <div class="stat-body">
              <div class="stat-value">${{ (stats.total_revenue || 0).toFixed(2) }}</div>
              <div class="stat-label">Total Revenue</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="top-books">
      <template #header>
        <div class="top-books-header">
          <h3>Top Selling Books</h3>
          <span class="top-books-count">{{ (stats.top_books || []).length }} books</span>
        </div>
      </template>
      <el-table :data="stats.top_books || []" stripe style="width: 100%">
        <el-table-column prop="title" label="Title" min-width="220" show-overflow-tooltip />
        <el-table-column prop="author" label="Author" min-width="160" show-overflow-tooltip />
        <el-table-column prop="category_name" label="Category" width="140" />
        <el-table-column prop="price" label="Price" width="100" align="right">
          <template #default="{ row }">
            <span class="price-cell">${{ row.price }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminGetStats } from '../../api/endpoints'

const stats = ref({})

onMounted(async () => {
  try {
    const res = await adminGetStats()
    stats.value = res.data
  } catch (e) {
    console.error('Failed to fetch dashboard stats:', e)
  }
})
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
}

.stat-cards {
  margin-bottom: 0;
}

.stat-col {
  margin-bottom: 20px;
}

.stat-card {
  height: 100%;
}

.stat-card :deep(.el-card__body) {
  padding: 20px 16px;
}

.stat-inner {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #fff;
}

.stat-icon.users { background: linear-gradient(135deg, #667eea, #764ba2); }
.stat-icon.books { background: linear-gradient(135deg, #f093fb, #f5576c); }
.stat-icon.orders { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.stat-icon.revenue { background: linear-gradient(135deg, #43e97b, #38f9d7); }

.stat-body {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.top-books {
  margin-top: 4px;
}

.top-books-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.top-books-header h3 {
  margin: 0;
  font-size: 16px;
}

.top-books-count {
  font-size: 13px;
  color: #909399;
}

.price-cell {
  font-weight: 600;
  color: #409eff;
}
</style>
