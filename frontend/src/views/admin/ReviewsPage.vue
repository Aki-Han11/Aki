<template>
  <div class="reviews-page">
    <div class="page-header">
      <h2>Review Management</h2>
      <p class="subtitle">View and moderate all book reviews</p>
    </div>

    <el-table :data="reviews" v-loading="loading" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="book_title" label="Book" min-width="180" />
      <el-table-column prop="user" label="User" width="120" />
      <el-table-column prop="rating" label="Rating" width="180">
        <template #default="{ row }">
          <el-rate :model-value="row.rating" disabled show-score text-color="#ff9900" />
        </template>
      </el-table-column>
      <el-table-column prop="review" label="Review" min-width="250">
        <template #default="{ row }">
          <span v-if="row.review">{{ row.review }}</span>
          <span v-else class="no-review">— No text —</span>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="Date" width="120">
        <template #default="{ row }">
          {{ new Date(row.created_at).toLocaleDateString() }}
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="100" fixed="right">
        <template #default="{ row }">
          <el-popconfirm title="Delete this review?" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button type="danger" size="small" plain>Delete</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { adminGetReviews, adminDeleteReview } from '../../api/endpoints'

const reviews = ref([])
const loading = ref(false)

async function fetchReviews() {
  loading.value = true
  try {
    const res = await adminGetReviews()
    reviews.value = res.data
  } catch (e) {
    ElMessage.error('Failed to load reviews')
  }
  loading.value = false
}

async function handleDelete(id) {
  try {
    await adminDeleteReview(id)
    ElMessage.success('Review deleted')
    fetchReviews()
  } catch (e) {
    ElMessage.error('Failed to delete review')
  }
}

onMounted(fetchReviews)
</script>

<style scoped>
.reviews-page { max-width: 1200px; }
.page-header { margin-bottom: 24px; }
.page-header h2 { margin: 0 0 4px 0; font-size: 22px; }
.subtitle { color: #999; margin: 0; font-size: 14px; }
.no-review { color: #ccc; font-style: italic; }
</style>
