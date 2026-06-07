<template>
  <div class="profile-page">
    <h1>My Profile</h1>

    <!-- Profile Header — avatar initial + identity -->
    <div class="profile-header">
      <div class="profile-avatar">
        <span class="avatar-placeholder">{{ (form.username || 'U')[0].toUpperCase() }}</span>
      </div>
      <div class="profile-identity">
        <h2>{{ form.username }}</h2>
        <p>{{ form.email }}</p>
      </div>
    </div>

    <!-- Profile Info -->
    <div class="profile-section">
      <h3>Profile Information</h3>
      <div class="info-grid">
        <div class="info-field">
          <label>Username</label>
          <el-input v-model="form.username" disabled />
        </div>
        <div class="info-field">
          <label>Email</label>
          <el-input v-model="form.email" placeholder="your@email.com" />
        </div>
      </div>
      <div class="section-action">
        <el-button type="primary" :loading="saving" @click="saveProfile">Save Changes</el-button>
      </div>
    </div>

    <!-- Change Password -->
    <div class="profile-section">
      <h3>Change Password</h3>
      <div class="info-grid info-grid--two">
        <div class="info-field">
          <label>Current Password</label>
          <el-input v-model="pwForm.old_password" type="password" show-password placeholder="Enter current password" />
        </div>
        <div class="info-field">
          <label>New Password</label>
          <el-input v-model="pwForm.new_password" type="password" show-password placeholder="At least 6 characters" />
        </div>
      </div>
      <div class="section-action">
        <el-button :loading="changingPw" @click="changePassword">Change Password</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getProfile, updateProfile, changePassword as changePwApi } from '../api/endpoints'

const form = reactive({ username: '', email: '' })
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
    await updateProfile({ email: form.email })
    ElMessage.success('Profile updated')
  } catch (e) {
    ElMessage.error('Failed to update')
  }
  saving.value = false
}

async function changePassword() {
  if (!pwForm.old_password || !pwForm.new_password) {
    ElMessage.warning('Please fill in both password fields')
    return
  }
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
.profile-page { max-width: 720px; margin: 0 auto; padding: 0 32px; }
h1 { margin-bottom: 36px; font-size: 28px; font-weight: 700; color: #1a1815; letter-spacing: -0.5px; }

/* ── Profile Header — avatar + identity ── */
.profile-header {
  display: flex; align-items: center; gap: 24px;
  padding-bottom: 32px; margin-bottom: 36px;
  border-bottom: 1px solid #f0f0f0;
}
.profile-avatar {
  width: 88px; height: 88px; border-radius: 50%;
  flex-shrink: 0; background: #f0f0f0;
  display: flex; align-items: center; justify-content: center;
}
.avatar-placeholder {
  font-size: 36px; font-weight: 700; color: #8b7e74;
}
.profile-identity h2 { font-size: 22px; font-weight: 700; color: #1a1815; margin: 0 0 4px; letter-spacing: -0.3px; }
.profile-identity p { font-size: 14px; color: #a0988c; margin: 0; }

/* ── Section ── */
.profile-section {
  margin-bottom: 40px;
}
.profile-section h3 {
  font-size: 17px; font-weight: 600; color: #1a1815;
  margin: 0 0 20px; padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}
.info-grid {
  display: grid; grid-template-columns: 1fr; gap: 18px;
}
.info-grid--two {
  grid-template-columns: 1fr 1fr;
}
.info-field label {
  display: block; font-size: 13px; font-weight: 500; color: #8b7e74;
  margin-bottom: 6px;
}
.section-action { margin-top: 20px; }

@media (max-width: 640px) {
  .profile-page { padding: 0 16px; }
  .info-grid--two { grid-template-columns: 1fr; }
  .profile-header { gap: 16px; }
  .profile-avatar { width: 64px; height: 64px; }
}
</style>
