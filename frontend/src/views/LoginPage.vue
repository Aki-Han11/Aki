<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h2>Welcome Back</h2>
        <p>Sign in to your EBook Store account</p>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top" class="auth-form">
        <el-form-item label="Username" prop="username">
          <el-input v-model="form.username" placeholder="Enter username" size="large" />
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="Enter password" size="large" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" size="large" class="auth-submit-btn">Sign In</el-button>
        </el-form-item>
      </el-form>
      <div class="auth-footer">
        Don't have an account? <router-link to="/register">Create one</router-link>
      </div>
      <el-divider class="auth-divider" />
      <div class="demo-info">
        <p class="demo-title">Demo Accounts</p>
        <div class="demo-row"><span class="demo-role">Admin</span><code>admin / admin123</code></div>
        <div class="demo-row"><span class="demo-role">User</span><code>demo / demo123</code></div>
      </div>
    </div>
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
  min-height: calc(100vh - 124px); padding: 40px 24px;
}
.auth-card {
  width: 440px; max-width: 100%;
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #f0f0f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 8px 32px rgba(0,0,0,0.04);
  padding: 40px 36px;
}
.auth-header {
  text-align: center; margin-bottom: 36px;
}
.auth-header h2 {
  margin: 0 0 8px; font-size: 26px; font-weight: 700;
  color: #0f172a; letter-spacing: -0.4px;
}
.auth-header p {
  margin: 0; font-size: 14px; color: #64748b;
}
.auth-form :deep(.el-form-item__label) {
  color: #475569; font-size: 13px; font-weight: 500;
}
.auth-submit-btn {
  width: 100%; border-radius: 10px; font-weight: 600; font-size: 15px;
  padding: 12px 0; height: auto;
}
.auth-footer {
  text-align: center; margin-top: 24px; font-size: 14px; color: #64748b;
}
.auth-footer a { color: #2563eb; font-weight: 500; }

.auth-divider { margin: 24px 0 20px; }

.demo-info { text-align: center; }
.demo-title {
  font-size: 12px; font-weight: 600; color: #94a3b8;
  text-transform: uppercase; letter-spacing: 0.8px; margin: 0 0 12px;
}
.demo-row {
  display: flex; align-items: center; justify-content: center; gap: 10px;
  margin-bottom: 6px; font-size: 13px;
}
.demo-role {
  font-weight: 600; color: #475569; min-width: 50px; text-align: right;
}
.demo-row code {
  background: #f8fafc; border: 1px solid #f0f0f0;
  border-radius: 6px; padding: 3px 10px; font-size: 12px;
  color: #64748b; font-family: 'SF Mono', 'Menlo', monospace;
}

@media (max-width: 480px) {
  .auth-page { padding: 24px 16px; }
  .auth-card { padding: 28px 20px; border-radius: 14px; }
  .auth-header h2 { font-size: 22px; }
  .demo-row { flex-direction: column; gap: 2px; }
  .demo-role { text-align: center; }
}
</style>
