<template>
  <div class="categories-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>Category Management</h3>
          <el-button type="primary" @click="openAdd">
            <el-icon><Plus /></el-icon> Add Category
          </el-button>
        </div>
      </template>
      <el-table :data="categories" stripe v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="name" label="Name" min-width="200" show-overflow-tooltip />
        <el-table-column prop="book_count" label="Books" width="100" align="center">
          <template #default="{ row }">
            <el-tag size="small" round>{{ row.book_count || 0 }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="160" fixed="right">
          <template #default="{ row }">
            <div class="action-btns">
              <el-button size="small" type="primary" plain @click="openEdit(row)">Edit</el-button>
              <el-popconfirm title="Delete this category?" @confirm="deleteCat(row)">
                <template #reference>
                  <el-button size="small" type="danger" plain>Delete</el-button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="categories.length === 0 && !loading" class="empty-state">
        <el-empty description="No categories found" />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? 'Edit Category' : 'Add Category'" width="440px" destroy-on-close>
      <el-form :model="form" label-position="top" @submit.prevent="saveCat">
        <el-form-item label="Category Name" required>
          <el-input v-model="form.name" placeholder="Enter category name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="saveCat">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { adminGetCategories, adminCreateCategory, adminUpdateCategory, adminDeleteCategory } from '../../api/endpoints'

const categories = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref(null)
const form = ref({ name: '' })

async function fetchCats() {
  loading.value = true
  try {
    const res = await adminGetCategories()
    categories.value = res.data.results || res.data
  } catch (e) { categories.value = [] }
  loading.value = false
}

function openAdd() {
  isEdit.value = false
  editingId.value = null
  form.value = { name: '' }
  dialogVisible.value = true
}

function openEdit(row) {
  isEdit.value = true
  editingId.value = row.id
  form.value = { name: row.name }
  dialogVisible.value = true
}

async function saveCat() {
  if (!form.value.name.trim()) {
    ElMessage.warning('Category name is required')
    return
  }
  try {
    if (isEdit.value) {
      await adminUpdateCategory(editingId.value, form.value)
    } else {
      await adminCreateCategory(form.value)
    }
    ElMessage.success(isEdit.value ? 'Category updated' : 'Category created')
    dialogVisible.value = false
    fetchCats()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || 'Failed to save category')
  }
}

async function deleteCat(row) {
  try {
    await adminDeleteCategory(row.id)
    ElMessage.success('Category deleted')
    fetchCats()
  } catch (e) { ElMessage.error('Failed to delete category') }
}

onMounted(fetchCats)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
h3 { margin: 0; font-weight: 600; color: #1e293b; font-size: 17px; }
.action-btns { display: flex; gap: 6px; }
.empty-state { padding: 40px 0; }
.categories-page :deep(.el-card) { border-radius: 12px; border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
</style>
