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
        <div class="book-cover-wrap">
          <img :src="book.cover_url" :alt="book.title" @error="e => e.target.src='https://picsum.photos/seed/default/200/300'" />
        </div>
        <div class="book-info">
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author">by {{ book.author }}</p>
          <el-tag v-if="book.category_name" size="small" type="info" class="book-cat">{{ book.category_name }}</el-tag>
          <p class="book-desc">{{ truncate(book.description, 200) }}</p>
          <div class="book-meta">
            <span class="book-price">${{ book.price }}</span>
            <span v-if="book.tags" class="book-tags">
              <el-tag v-for="tag in (book.tags||'').split(',').slice(0,3)" :key="tag" size="small" effect="plain">{{ tag.trim() }}</el-tag>
            </span>
          </div>
        </div>
        <div class="book-arrow">
          <el-icon :size="20"><ArrowRight /></el-icon>
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
.featured-page { max-width: 1100px; margin: 0 auto; padding: 0 20px; }
.page-header { text-align: center; margin-bottom: 40px; }
.page-header h1 { font-size: 32px; font-weight: 800; color: #1a1815; margin-bottom: 8px; letter-spacing: -0.5px; }
.page-header p { color: #a0988c; font-size: 16px; }

.book-list { display: flex; flex-direction: column; gap: 16px; }
.book-row {
  display: flex; align-items: flex-start; gap: 24px;
  background: #fefdfc; border-radius: 18px; padding: 24px;
  cursor: pointer; transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  border: 1px solid #f1ede7;
  box-shadow: 0 1px 3px rgba(0,0,0,0.018), 0 1px 2px rgba(0,0,0,0.022);
}
.book-row:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 36px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.03);
  border-color: #e3dbd1;
}
.book-cover-wrap { flex-shrink: 0; }
.book-cover-wrap img {
  width: 110px; height: 160px; object-fit: cover; border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.book-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px; }
.book-title { font-size: 18px; font-weight: 700; color: #1a1815; margin: 0; line-height: 1.3; }
.book-author { font-size: 14px; color: #a0988c; margin: 0; }
.book-cat { width: fit-content; }
.book-desc {
  font-size: 14px; color: #8b7e74; line-height: 1.7; margin: 2px 0;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
  overflow: hidden;
}
.book-meta { display: flex; align-items: center; gap: 14px; margin-top: 2px; }
.book-price { font-size: 20px; font-weight: 700; color: #1a1815; }
.book-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.book-arrow { color: #c0b8ac; flex-shrink: 0; align-self: center; transition: all 0.3s; }
.book-row:hover .book-arrow { color: #2563eb; transform: translateX(3px); }

.empty-state { padding: 80px 0; }
.pagination-bar { display: flex; justify-content: center; margin-top: 40px; }
</style>
