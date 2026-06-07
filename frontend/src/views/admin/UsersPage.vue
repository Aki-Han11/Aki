<template>
  <div class="users-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>User Management</h3>
          <div class="header-actions">
            <el-input v-model="search" placeholder="Search by username or email..." clearable style="width: 280px"
              @keyup.enter="fetchUsers" @clear="fetchUsers">
              <template #prefix><el-icon><Search /></el-icon></template>
            </el-input>
          </div>
        </div>
      </template>
      <el-table :data="users" stripe v-loading="loading" style="width: 100%">
        <el-table-column prop="username" label="Username" min-width="150" show-overflow-tooltip />
        <el-table-column prop="email" label="Email" min-width="220" show-overflow-tooltip />
        <el-table-column prop="role" label="Role" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.role==='admin'?'danger':'info'" size="small">{{ row.role }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="Active" width="80" align="center">
          <template #default="{ row }">
            <el-switch :model-value="row.is_active" @change="toggleActive(row)" :disabled="row.role==='admin'" size="small" />
          </template>
        </el-table-column>
        <el-table-column prop="date_joined" label="Joined" min-width="130">
          <template #default="{ row }">{{ new Date(row.date_joined).toLocaleDateString() }}</template>
        </el-table-column>
        <el-table-column label="Actions" min-width="160" fixed="right">
          <template #default="{ row }">
            <div class="action-btns">
              <el-button size="small" type="primary" plain @click="editUser(row)">Edit</el-button>
              <el-popconfirm title="Deactivate this user?" @confirm="deleteUser(row)">
                <template #reference>
                  <el-button size="small" type="danger" plain :disabled="row.role==='admin'">Delete</el-button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-bar" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchUsers"
        />
      </div>
      <div v-if="users.length===0 && !loading" class="empty-state">
        <el-empty description="No users found" />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" title="Edit User" width="480px" destroy-on-close>
      <el-form :model="editForm" label-position="top">
        <el-form-item label="Email"><el-input v-model="editForm.email" /></el-form-item>
        <el-form-item label="Role">
          <el-select v-model="editForm.role" style="width:100%">
            <el-option value="user" label="User" /><el-option value="admin" label="Admin" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">Cancel</el-button>
        <el-button type="primary" @click="saveUser">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { adminGetUsers, adminUpdateUser, adminToggleUserActive, adminDeleteUser } from '../../api/endpoints'

const users = ref([])
const loading = ref(false)
const search = ref('')
const page = ref(1)
const total = ref(0)
const pageSize = 20
const dialogVisible = ref(false)
const editForm = ref({})
const editingId = ref(null)

async function fetchUsers() {
  loading.value = true
  try {
    const res = await adminGetUsers({ search: search.value, page: page.value })
    users.value = res.data.results || res.data
    total.value = res.data.count || 0
  } catch (e) { users.value = []; total.value = 0 }
  loading.value = false
}

function editUser(row) { editingId.value=row.id; editForm.value={email:row.email,role:row.role}; dialogVisible.value=true }

async function saveUser() {
  try { await adminUpdateUser(editingId.value, editForm.value); ElMessage.success('Updated'); dialogVisible.value=false; fetchUsers() }
  catch(e) { ElMessage.error(e.response?.data?.detail||'Failed') }
}

async function toggleActive(row) {
  try { await adminToggleUserActive(row.id); ElMessage.success(row.is_active?'Deactivated':'Activated'); fetchUsers() }
  catch(e) { ElMessage.error('Failed') }
}

async function deleteUser(row) {
  try { await adminDeleteUser(row.id); ElMessage.success('Deactivated'); fetchUsers() }
  catch(e) { ElMessage.error('Failed') }
}

onMounted(fetchUsers)
</script>

<style scoped>
.card-header { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
h3 { margin:0; font-weight:600; color:#1a1815; font-size:17px; }
.header-actions { display:flex; gap:12px; align-items:center; }
.action-btns { display:flex; gap:6px; }
.empty-state { padding:40px 0; }
.pagination-bar { display:flex; justify-content:center; margin-top:20px; }
.users-page :deep(.el-card) { border-radius:12px; border:none; box-shadow:0 1px 3px rgba(0,0,0,0.04); }

@media (max-width: 768px) {
  .card-header { flex-direction: column; align-items: stretch; }
  .header-actions { width: 100%; }
  .header-actions .el-input { width: 100% !important; }
  .users-page :deep(.el-dialog) { width: 92% !important; }
}
</style>
