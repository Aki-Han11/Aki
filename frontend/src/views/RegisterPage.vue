<template>
  <div class="auth-page">
    <el-card class="auth-card">
      <template #header><h2>Register</h2></template>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <el-form-item label="Username" prop="username">
          <el-input v-model="form.username" placeholder="Choose a username" />
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="form.email" placeholder="Enter email" />
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input v-model="form.password" type="password" show-password placeholder="At least 6 characters" />
        </el-form-item>
        <el-form-item label="Confirm Password" prop="password2">
          <el-input v-model="form.password2" type="password" show-password placeholder="Re-enter password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleRegister" style="width: 100%">Register</el-button>
        </el-form-item>
      </el-form>
      <div class="auth-link">
        Already have an account? <router-link to="/login">Login</router-link>
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
  min-height: calc(100vh - 200px); padding: 24px;
}
.auth-card { width: 420px; }
.auth-card h2 { margin: 0; font-size: 22px; font-weight: 700; color: #1a1815; }
.auth-link { text-align: center; margin-top: 12px; font-size: 14px; color: #8b7e74; }
.auth-link a { color: #2563eb; font-weight: 500; }

@media (max-width: 480px) {
  .auth-card { width: 100%; max-width: 100%; }
  .auth-page { padding: 16px; }
}
</style>
