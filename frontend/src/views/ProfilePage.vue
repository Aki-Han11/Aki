<template>
  <div class="profile-page">
    <h1>My Profile</h1>
    <el-row :gutter="24">
      <el-col :span="12">
        <el-card>
          <template #header><h3>Profile Info</h3></template>
          <el-form :model="form" label-position="top">
            <el-form-item label="Username">
              <el-input v-model="form.username" disabled />
            </el-form-item>
            <el-form-item label="Email">
              <el-input v-model="form.email" />
            </el-form-item>
            <el-form-item label="Avatar URL">
              <el-input v-model="form.avatar" placeholder="Enter avatar URL" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="saveProfile">Save Changes</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header><h3>Change Password</h3></template>
          <el-form :model="pwForm" ref="pwFormRef" label-position="top">
            <el-form-item label="Current Password" prop="old_password">
              <el-input v-model="pwForm.old_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="New Password" prop="new_password">
              <el-input v-model="pwForm.new_password" type="password" show-password />
            </el-form-item>
            <el-form-item>
              <el-button :loading="changingPw" @click="changePassword">Change Password</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getProfile, updateProfile, changePassword as changePwApi } from '../api/endpoints'

const form = reactive({ username: '', email: '', avatar: '' })
const pwForm = reactive({ old_password: '', new_password: '' })
const pwFormRef = ref(null)
const saving = ref(false)
const changingPw = ref(false)

onMounted(async () => {
  try {
    const res = await getProfile()
    Object.assign(form, res.data)
  } catch (e) {}
})

async function saveProfile() {
  saving.value = true
  try {
    await updateProfile({ email: form.email, avatar: form.avatar })
    ElMessage.success('Profile updated')
  } catch (e) {
    ElMessage.error('Failed to update')
  }
  saving.value = false
}

async function changePassword() {
  changingPw.value = true
  try {
    await changePwApi(pwForm)
    ElMessage.success('Password changed')
    pwForm.old_password = ''
    pwForm.new_password = ''
  } catch (e) {
    ElMessage.error(e.response?.data?.error || 'Failed to change password')
  }
  changingPw.value = false
}
</script>

<style scoped>
h1 {
  margin-bottom: 24px;
}
h3 {
  margin: 0;
}
</style>
