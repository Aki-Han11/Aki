<template>
  <div class="downloads-page">
    <h1>Download History</h1>
    <div v-if="loading"><el-skeleton :rows="5" animated /></div>
    <template v-else-if="downloads.length">
      <div class="dl-list">
        <div v-for="dl in downloads" :key="dl.id" class="dl-item">
          <img :src="dl.book?.cover_url" :alt="dl.book?.title" class="dl-cover" @error="e => e.target.src='https://picsum.photos/seed/default/200/300'" />
          <div class="dl-info">
            <router-link :to="`/books/${dl.book?.id}`"><h3>{{ dl.book?.title }}</h3></router-link>
            <p>{{ dl.book?.author }}</p>
            <p class="dl-date">Downloaded on {{ new Date(dl.created_at).toLocaleString() }}</p>
          </div>
        </div>
      </div>
    </template>
    <el-empty v-else description="No downloads yet" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDownloads } from '../api/endpoints'

const downloads = ref([])
const loading = ref(true)

onMounted(async () => {
  loading.value = true
  try {
    const res = await getDownloads()
    downloads.value = res.data.results || res.data
  } catch (e) { downloads.value = [] }
  loading.value = false
})
</script>

<style scoped>
h1 { margin-bottom: 28px; font-size: 28px; font-weight: 700; color: #1a1815; letter-spacing: -0.4px; }
.dl-list { display: flex; flex-direction: column; gap: 12px; }
.dl-item {
  display: flex; align-items: center; gap: 18px;
  background: #fffdfa; padding: 18px; border-radius: 16px;
  border: 1px solid #f0ece6;
  box-shadow: 0 1px 3px rgba(0,0,0,0.018), 0 1px 2px rgba(0,0,0,0.022);
  transition: all 0.25s ease;
}
.dl-item:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.04); border-color: #e0d8cc; }
.dl-cover { width: 65px; height: 92px; object-fit: cover; border-radius: 8px; }
.dl-info { flex: 1; }
.dl-info h3 { font-size: 16px; font-weight: 600; color: #1a1815; }
.dl-info p { color: #a0988c; font-size: 14px; }
.dl-date { font-size: 12px; color: #b8b0a4; margin-top: 4px; }
</style>
