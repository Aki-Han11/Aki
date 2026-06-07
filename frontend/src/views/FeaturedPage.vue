<template>
  <div class="featured-page">
    <div class="page-header">
      <h1>{{ title }}</h1>
      <p>{{ subtitle }}</p>
    </div>

    <div v-loading="loading" class="book-list">
      <div v-if="books.length === 0 && !loading" class="empty-state">
        <el-empty :description="emptyDesc" />
      </div>
      <div v-for="book in books" :key="book.id" class="book-row" @click="$router.push(`/books/${book.id}`)">
        <img :src="book.cover_url" :alt="book.title" class="book-cover" @error="e => e.target.src='https://picsum.photos/seed/default/200/300'" />
        <div class="book-center">
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author">{{ book.author }}</p>
          <div class="book-meta">
            <el-tag v-if="book.category_name" size="small" class="book-cat">{{ book.category_name }}</el-tag>
            <span v-if="book.tags" class="book-tags">
              <el-tag v-for="tag in (book.tags||'').split(',').slice(0,3)" :key="tag" size="small" effect="plain">{{ tag.trim() }}</el-tag>
            </span>
          </div>
        </div>
        <p class="book-desc">{{ truncate(book.description, 180) }}</p>
        <div class="book-right">
          <span class="book-price">${{ book.price }}</span>
          <span class="book-arrow"><el-icon :size="18"><ArrowRight /></el-icon></span>
        </div>
      </div>
    </div>

    <div class="pagination-bar" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="fetchBooks"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getNewBooks, getHotBooks, getRecommendBooks } from '../api/endpoints'

const route = useRoute()
const props = defineProps({ type: { type: String, required: true } })

const books = ref([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)
const pageSize = 12

const config = computed(() => ({
  new: { title: 'New Arrivals', subtitle: 'The latest books added to our collection', empty: 'No new books available', api: getNewBooks, params: () => ({}) },
  hot: { title: 'Popular Books', subtitle: 'Most purchased and favorited by our readers', empty: 'No popular books right now', api: getHotBooks, params: () => ({ period: 'all' }) },
  recommended: { title: 'Recommended For You', subtitle: 'Personalized picks based on your reading history', empty: 'Login and rate books to get recommendations', api: getRecommendBooks, params: () => ({}) },
}))

const title = computed(() => config.value[props.type]?.title || '')
const subtitle = computed(() => config.value[props.type]?.subtitle || '')
const emptyDesc = computed(() => config.value[props.type]?.empty || '')

function truncate(text, len) {
  if (!text) return ''
  return text.length > len ? text.slice(0, len) + '...' : text
}

async function fetchBooks() {
  const cfg = config.value[props.type]
  if (!cfg) return
  loading.value = true
  try {
    const res = await cfg.api(cfg.params())
    if (Array.isArray(res.data)) {
      books.value = res.data
      total.value = res.data.length
    } else {
      books.value = res.data.results || res.data || []
      total.value = res.data.count || books.value.length
    }
  } catch (e) {
    books.value = []
    total.value = 0
  }
  loading.value = false
}

watch(() => route.path, () => { if (props.type) fetchBooks() })
onMounted(fetchBooks)
</script>

<style scoped>
.featured-page { max-width: 1200px; margin: 0 auto; padding: 0 32px; }
.page-header { margin-bottom: 40px; }
.page-header h1 { font-size: 28px; font-weight: 700; color: #1a1815; margin-bottom: 4px; letter-spacing: -0.5px; }
.page-header p { color: #a0988c; font-size: 14px; }

.book-list { display: flex; flex-direction: column; }
.book-row {
  display: flex; align-items: flex-start; gap: 28px;
  padding: 24px 0;
  cursor: pointer; transition: background 0.2s ease;
  border-bottom: 1px solid #f0f0f0;
}
.book-row:last-child { border-bottom: none; }
.book-row:hover { background: #ffffff; margin: 0 -12px; padding-left: 12px; padding-right: 12px; border-radius: 6px; }
.book-cover {
  width: 90px; height: 128px; object-fit: cover; border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08); flex-shrink: 0;
}
.book-center { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 4px; padding-top: 2px; }
.book-title { font-size: 17px; font-weight: 600; color: #1a1815; margin: 0; line-height: 1.3; }
.book-author { font-size: 13px; color: #a0988c; margin: 0; }
.book-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-top: 4px; }
.book-cat { flex-shrink: 0; }
.book-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.book-desc {
  flex: 1.2; min-width: 180px; max-width: 380px;
  font-size: 13px; color: #8b7e74; line-height: 1.7; margin: 0;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
  overflow: hidden; padding-top: 2px;
}
.book-right {
  display: flex; flex-direction: column; align-items: flex-end; gap: 8px;
  flex-shrink: 0; padding-top: 2px;
}
.book-price { font-size: 18px; font-weight: 700; color: #1a1815; }
.book-arrow { color: #c0b8ac; transition: all 0.2s; opacity: 0; }
.book-row:hover .book-arrow { color: #2563eb; opacity: 1; }

.empty-state { padding: 80px 0; }
.pagination-bar { display: flex; justify-content: center; margin-top: 48px; }

@media (max-width: 860px) {
  .book-desc { display: none; }
}
@media (max-width: 640px) {
  .featured-page { padding: 0 16px; }
  .book-row { gap: 16px; padding: 18px 0; }
  .book-row:hover { margin: 0 -8px; padding-left: 8px; padding-right: 8px; }
  .book-cover { width: 70px; height: 100px; }
}
@media (max-width: 420px) {
  .book-row { flex-wrap: wrap; }
  .book-center { flex: 1 1 calc(100% - 86px); }
  .book-right { width: 100%; flex-direction: row; justify-content: space-between; align-items: center; }
}
</style>
