<template>
  <div class="book-list-page">
    <div class="page-header">
      <h1>Browse Books</h1>
      <p>Explore our collection of ebooks</p>
    </div>

    <div class="filters">
      <el-input
        v-model="searchQuery"
        placeholder="Search books..."
        prefix-icon="Search"
        clearable
        @keyup.enter="doSearch"
        style="max-width: 400px"
      />
      <el-select v-model="selectedCategory" placeholder="All Categories" clearable @change="fetchBooks" style="width: 220px">
        <el-option
          v-for="cat in categories"
          :key="cat.id"
          :label="`${cat.name} (${cat.book_count})`"
          :value="cat.id"
        />
      </el-select>
    </div>

    <BookGrid :books="books" :loading="loading" />

    <div class="pagination" v-if="total > 0">
      <el-pagination
        v-model:current-page="page"
        :page-size="12"
        :total="total"
        layout="prev, pager, next"
        @current-change="fetchBooks"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getBooks, getCategories } from '../api/endpoints'
import BookGrid from '../components/BookGrid.vue'

const route = useRoute()

const books = ref([])
const categories = ref([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)
const searchQuery = ref(route.query.q || '')
const selectedCategory = ref(route.query.category || '')

async function fetchBooks() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (searchQuery.value) params.search = searchQuery.value
    if (selectedCategory.value) params.category = selectedCategory.value
    const res = await getBooks(params)
    books.value = res.data.results
    total.value = res.data.count
  } catch (e) {
    books.value = []
  }
  loading.value = false
}

async function fetchCategories() {
  try {
    const res = await getCategories()
    categories.value = res.data
  } catch (e) {
    categories.value = []
  }
}

function doSearch() {
  page.value = 1
  fetchBooks()
}

onMounted(() => {
  fetchCategories()
  fetchBooks()
})
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 28px;
  color: #303133;
}

.page-header p {
  color: #999;
  margin-top: 4px;
}

.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}
</style>
