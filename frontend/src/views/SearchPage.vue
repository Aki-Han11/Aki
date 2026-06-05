<template>
  <div class="search-page">
    <div class="page-header">
      <h1>Search Results</h1>
      <p v-if="query">Showing results for "<strong>{{ query }}</strong>"</p>
    </div>
    <BookGrid :books="results" :loading="loading" />
    <el-empty v-if="!loading && results.length === 0" description="No books found" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { searchBooks } from '../api/endpoints'
import BookGrid from '../components/BookGrid.vue'

const route = useRoute()
const results = ref([])
const loading = ref(false)
const query = ref(route.query.q || '')

async function doSearch() {
  if (!query.value) return
  loading.value = true
  try {
    const res = await searchBooks(query.value)
    results.value = res.data.results || res.data
  } catch (e) {
    results.value = []
  }
  loading.value = false
}

watch(() => route.query.q, (newQ) => {
  query.value = newQ || ''
  doSearch()
})

onMounted(() => doSearch())
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
}
.page-header h1 {
  font-size: 28px;
}
.page-header p {
  color: #999;
  margin-top: 8px;
}
</style>
