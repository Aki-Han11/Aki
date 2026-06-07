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
.downloads-page { max-width: 900px; margin: 0 auto; padding: 0 32px; }
h1 { margin-bottom: 36px; font-size: 28px; font-weight: 700; color: #1a1815; letter-spacing: -0.5px; }
.dl-list { display: flex; flex-direction: column; }
.dl-item {
  display: flex; align-items: center; gap: 24px;
  padding: 22px 0;
  border-bottom: 1px solid #f2ede7;
}
.dl-cover { width: 80px; height: 114px; object-fit: cover; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); flex-shrink: 0; }
.dl-info { flex: 1; min-width: 0; }
.dl-info h3 { font-size: 16px; font-weight: 600; color: #1a1815; }
.dl-info p { color: #a0988c; font-size: 13px; }
.dl-date { font-size: 12px; color: #b8b0a4; margin-top: 6px; }
</style>
