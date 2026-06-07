<template>
  <div class="recs-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>Recommendation Engine Management</h3>
        </div>
      </template>

      <div class="recs-content">
        <div class="info-section">
          <el-icon :size="48" color="#409eff"><MagicStick /></el-icon>
          <div class="info-text">
            <h4>KNNBaseline Collaborative Filtering</h4>
            <p>This model uses user rating data to generate personalized book recommendations. Training requires at least 5 ratings from users to produce meaningful results.</p>
          </div>
        </div>

        <el-divider />

        <div class="action-section">
          <el-button type="primary" size="large" @click="trainModel" :loading="training" :icon="MagicStick">
            Train Recommendation Model
          </el-button>
          <span class="hint">Training may take a few moments depending on the dataset size.</span>
        </div>

        <!-- Success result -->
        <div v-if="result && result.message" class="result-box success-box">
          <el-alert :title="result.message" type="success" :closable="false" show-icon />
          <div class="result-details">
            <el-row :gutter="24">
              <el-col :span="8">
                <div class="detail-item">
                  <span class="detail-value">{{ result.ratings_used }}</span>
                  <span class="detail-label">Ratings Used</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="detail-item">
                  <span class="detail-value">{{ result.users }}</span>
                  <span class="detail-label">Unique Users</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="detail-item">
                  <span class="detail-value">{{ result.books }}</span>
                  <span class="detail-label">Unique Books</span>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- Error alert (HTTP error) -->
        <el-alert
          v-if="error"
          :title="error"
          type="error"
          show-icon
          :closable="false"
          style="margin-top: 20px;"
        />

        <!-- Error in response body (200 with error key) -->
        <el-alert
          v-if="result && result.error"
          :title="result.error"
          type="warning"
          show-icon
          :closable="false"
          style="margin-top: 20px;"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { MagicStick } from '@element-plus/icons-vue'
import { adminTrainRecommendations } from '../../api/endpoints'

const training = ref(false)
const result = ref(null)
const error = ref('')

async function trainModel() {
  training.value = true
  result.value = null
  error.value = ''
  try {
    const res = await adminTrainRecommendations()
    result.value = res.data
  } catch (e) {
    error.value = e.response?.data?.error || 'Training failed. Please try again.'
  }
  training.value = false
}
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
h3 { margin: 0; font-weight: 600; color: #1e293b; font-size: 17px; }

.recs-content { max-width: 800px; }

.info-section { display: flex; align-items: center; gap: 20px; padding: 8px 0; }
.info-text h4 { margin: 0 0 8px 0; font-size: 16px; color: #1e293b; }
.info-text p { margin: 0; color: #64748b; line-height: 1.7; font-size: 14px; }

.action-section { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.hint { color: #94a3b8; font-size: 13px; }

.result-box { margin-top: 24px; }
.result-details {
  background: #f8fafc; padding: 24px; border-radius: 14px;
  margin-top: 16px; border: 1px solid #e2e8f0;
}
.detail-item { text-align: center; padding: 8px 0; }
.detail-value { display: block; font-size: 28px; font-weight: 700; color: #409eff; }
.detail-label { display: block; font-size: 13px; color: #94a3b8; margin-top: 4px; }

.recs-page :deep(.el-card) { border-radius: 16px; border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
</style>
