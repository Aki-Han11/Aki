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
    stats.value = {}
  }
})
</script>

<style scoped>
.dashboard { max-width: 1400px; }
.stat-cards { margin-bottom: 0; }
.stat-col { margin-bottom: 20px; }
.stat-card { border-radius: 12px; border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.03); height: 100%; }
.stat-card :deep(.el-card__body) { padding: 24px 20px; }
.stat-inner { display: flex; align-items: center; gap: 18px; }
.stat-icon {
  width: 52px; height: 52px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: #fff;
}
.stat-icon.users { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
.stat-icon.books { background: linear-gradient(135deg, #ec4899, #f43f5e); }
.stat-icon.orders { background: linear-gradient(135deg, #3b82f6, #06b6d4); }
.stat-icon.revenue { background: linear-gradient(135deg, #10b981, #14b8a6); }
.stat-body { flex: 1; min-width: 0; }
.stat-value { font-size: 26px; font-weight: 700; color: #1a1815; line-height: 1.2; }
.stat-label { font-size: 13px; color: #a0988c; margin-top: 2px; }

.top-books { margin-top: 4px; border-radius: 12px; border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.03); }
.top-books-header { display: flex; align-items: center; justify-content: space-between; }
.top-books-header h3 { margin: 0; font-size: 17px; font-weight: 600; color: #1a1815; }
.top-books-count { font-size: 13px; color: #a0988c; background: #efefef; padding: 2px 10px; border-radius: 12px; }
.price-cell { font-weight: 600; color: #1a1815; }
</style>
