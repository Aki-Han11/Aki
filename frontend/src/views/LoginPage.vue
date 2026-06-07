<template>
  <div class="auth-page">
    <el-card class="auth-card">
      <template #header>
        <h2>Login</h2>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <el-form-item label="Username" prop="username">
          <el-input v-model="form.username" placeholder="Enter username" />
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="Enter password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" style="width: 100%">Login</el-button>
        </el-form-item>
      </el-form>
      <div class="auth-link">
        Don't have an account? <router-link to="/register">Register now</router-link>
      </div>
      <el-divider />
      <div class="demo-info">
        <p><strong>Demo Account:</strong></p>
        <p>Admin: admin / admin123</p>
        <p>User: demo / demo123</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const auth = useAuthStore()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
})

const rules = {
  username: [{ required: true, message: 'Username required', trigger: 'blur' }],
  password: [{ required: true, message: 'Password required', trigger: 'blur' }],
}

async function handleLogin() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await auth.login(form.username, form.password)
    ElMessage.success('Login successful')
    if (auth.isAdmin) {
      router.push('/admin')
    } else {
      router.push('/')
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.error || 'Login failed')
  }
  loading.value = false
}
</script>

<style scoped>
.auth-page {
  display: flex; justify-content: center; align-items: center;
  min-height: calc(100vh - 200px); padding: 24px;
}
.auth-card { width: 420px; }
.auth-card h2 { margin: 0; font-size: 22px; font-weight: 700; color: #1a1815; }
.auth-link { text-align: center; margin-top: 12px; font-size: 14px; color: #8b7e74; }
.auth-link a { color: #2563eb; font-weight: 500; }
.demo-info { font-size: 13px; color: #a0988c; text-align: center; line-height: 1.7; }
.demo-info strong { color: #6b5e54; }
</style>
