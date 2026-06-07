<template>
  <div class="books-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>Book Management</h3>
          <div class="header-actions">
            <el-input v-model="search" placeholder="Search books..." clearable style="width: 240px" @keyup.enter="fetchBooks" @clear="fetchBooks">
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button type="primary" @click="openAdd">
              <el-icon><Plus /></el-icon> Add Book
            </el-button>
          </div>
        </div>
      </template>
      <el-table :data="books" stripe v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="title" label="Title" min-width="200" show-overflow-tooltip />
        <el-table-column prop="author" label="Author" min-width="140" show-overflow-tooltip />
        <el-table-column label="Category" width="140">
          <template #default="{ row }">
            <el-tag size="small" type="info">{{ row.category_name || row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="Price" width="90" align="right">
          <template #default="{ row }">
            <span class="price-cell">${{ row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Reviews" width="80" align="center">
          <template #default="{ row }">
            <el-button size="small" text type="primary" @click="openReviews(row)">
              <el-icon><ChatLineSquare /></el-icon>
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row)">Edit</el-button>
            <el-popconfirm title="Delete this book?" @confirm="deleteBook(row)">
              <template #reference>
                <el-button size="small" type="danger">Delete</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Add/Edit dialog -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? 'Edit Book' : 'Add Book'" width="640px" destroy-on-close>
      <el-form :model="bookForm" label-position="top" class="book-form">
        <el-row :gutter="20">
          <el-col :span="16">
            <el-form-item label="Title" required>
              <el-input v-model="bookForm.title" placeholder="Enter book title" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="Author" required>
              <el-input v-model="bookForm.author" placeholder="Author name" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="Description">
          <el-input v-model="bookForm.description" type="textarea" :rows="4" placeholder="Book description" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Category" required>
              <el-select v-model="bookForm.category" placeholder="Select category" style="width: 100%">
                <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Price ($)" required>
              <el-input-number v-model="bookForm.price" :min="0" :precision="2" :step="0.99" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Cover URL">
              <el-input v-model="bookForm.cover_url" placeholder="https://..." />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Download URL">
              <el-input v-model="bookForm.download_url" placeholder="https://..." />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="Tags">
          <el-input v-model="bookForm.tags" placeholder="e.g. python, programming, tech (comma separated)" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="saveBook" :loading="saving">Save</el-button>
      </template>
    </el-dialog>

    <!-- Reviews dialog -->
    <el-dialog v-model="reviewsVisible" :title="`Reviews — ${reviewBook?.title}`" width="700px" destroy-on-close>
      <div v-loading="reviewsLoading">
        <el-table v-if="reviews.length" :data="reviews" stripe>
          <el-table-column prop="user" label="User" width="120" />
          <el-table-column label="Rating" width="160">
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
          <el-table-column prop="created_at" label="Date" width="110">
            <template #default="{ row }">
              {{ new Date(row.created_at).toLocaleDateString() }}
            </template>
          </el-table-column>
          <el-table-column label="" width="70" align="center">
            <template #default="{ row }">
              <el-popconfirm title="Delete this review?" @confirm="deleteReview(row.id)">
                <template #reference>
                  <el-button size="small" type="danger" plain>Delete</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
        <el-empty v-else description="No reviews yet" :image-size="80" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Plus, ChatLineSquare } from '@element-plus/icons-vue'
import {
  adminGetBooks, adminCreateBook, adminUpdateBook, adminDeleteBook,
  adminGetCategories, adminGetReviews, adminDeleteReview
} from '../../api/endpoints'

const books = ref([])
const categories = ref([])
const loading = ref(false)
const search = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(null)
const saving = ref(false)
const bookForm = ref({
  title: '', author: '', description: '', category: null,
  price: 0, cover_url: '', download_url: '', tags: ''
})

// Review dialog
const reviewsVisible = ref(false)
const reviewsLoading = ref(false)
const reviews = ref([])
const reviewBook = ref(null)

async function fetchBooks() {
  loading.value = true
  try {
    const res = await adminGetBooks({ search: search.value })
    books.value = res.data.results || res.data
  } catch (e) { books.value = [] }
  loading.value = false
}

async function fetchCategories() {
  try {
    const res = await adminGetCategories()
    categories.value = res.data.results || res.data
  } catch (e) { categories.value = [] }
}

function openAdd() {
  isEdit.value = false
  editingId.value = null
  bookForm.value = {
    title: '', author: '', description: '', category: categories.value[0]?.id || null,
    price: 0, cover_url: '', download_url: '', tags: ''
  }
  dialogVisible.value = true
}

function openEdit(row) {
  isEdit.value = true
  editingId.value = row.id
  bookForm.value = {
    title: row.title || '', author: row.author || '', description: row.description || '',
    category: row.category || null, price: row.price || 0,
    cover_url: row.cover_url || '', download_url: row.download_url || '', tags: row.tags || '',
  }
  dialogVisible.value = true
}

async function saveBook() {
  saving.value = true
  try {
    if (isEdit.value) {
      await adminUpdateBook(editingId.value, bookForm.value)
    } else {
      await adminCreateBook(bookForm.value)
    }
    ElMessage.success(isEdit.value ? 'Book updated' : 'Book created')
    dialogVisible.value = false
    fetchBooks()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || 'Failed to save book')
  }
  saving.value = false
}

async function deleteBook(row) {
  try {
    await adminDeleteBook(row.id)
    ElMessage.success('Book deleted')
    fetchBooks()
  } catch (e) { ElMessage.error('Failed to delete book') }
}

// Review management
async function openReviews(book) {
  reviewBook.value = book
  reviewsVisible.value = true
  reviewsLoading.value = true
  try {
    const res = await adminGetReviews({ book_id: book.id })
    reviews.value = res.data
  } catch (e) {
    reviews.value = []
  }
  reviewsLoading.value = false
}

async function deleteReview(id) {
  try {
    await adminDeleteReview(id)
    ElMessage.success('Review deleted')
    reviews.value = reviews.value.filter(r => r.id !== id)
  } catch (e) {
    ElMessage.error('Failed to delete review')
  }
}

onMounted(() => {
  fetchBooks()
  fetchCategories()
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.header-actions { display: flex; gap: 12px; align-items: center; }
h3 { margin: 0; }
.price-cell { font-weight: 600; color: #409eff; }
.book-form { max-height: 60vh; overflow-y: auto; padding-right: 4px; }
.no-review { color: #ccc; font-style: italic; }
</style>
