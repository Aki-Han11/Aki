<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h2>Create Account</h2>
        <p>Join EBook Store and start reading</p>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top" class="auth-form">
        <el-form-item label="Username" prop="username">
          <el-input v-model="form.username" placeholder="Choose a username" size="large" />
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="form.email" placeholder="Enter your email" size="large" />
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="At least 6 characters" size="large" />
        </el-form-item>
        <el-form-item label="Confirm Password" prop="password2">
          <el-input v-model="form.password2" type="password" show-password placeholder="Re-enter password" size="large" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleRegister" size="large" class="auth-submit-btn">Create Account</el-button>
        </el-form-item>
      </el-form>
      <div class="auth-footer">
        Already have an account? <router-link to="/login">Sign In</router-link>
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
  email: '',
  password: '',
  password2: '',
})

const validatePass2 = (rule, value, callback) => {
  if (value !== form.password) callback(new Error('Passwords do not match'))
  else callback()
}

const rules = {
  username: [{ required: true, message: 'Username required', trigger: 'blur' }],
  email: [{ required: true, message: 'Email required', trigger: 'blur' }, { type: 'email', message: 'Invalid email', trigger: 'blur' }],
  password: [{ required: true, message: 'Password required', trigger: 'blur' }, { min: 6, message: 'At least 6 characters', trigger: 'blur' }],
  password2: [{ required: true, message: 'Please confirm password', trigger: 'blur' }, { validator: validatePass2, trigger: 'blur' }],
}

async function handleRegister() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await auth.register(form.username, form.email, form.password)
    ElMessage.success('Registration successful')
    router.push('/')
  } catch (e) {
    ElMessage.error(e.response?.data?.error || 'Registration failed')
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

@media (max-width: 480px) {
  .auth-page { padding: 24px 16px; }
  .auth-card { padding: 28px 20px; border-radius: 14px; }
  .auth-header h2 { font-size: 22px; }
}
</style>
