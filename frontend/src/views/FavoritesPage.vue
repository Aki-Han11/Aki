<template>
  <div class="favorites-page">
    <h1>My Favorites</h1>
    <div v-if="loading"><el-skeleton :rows="5" animated /></div>
    <template v-else-if="favorites.length">
      <div class="fav-list">
        <div v-for="fav in favorites" :key="fav.id" class="fav-item">
          <img :src="fav.book.cover_url" :alt="fav.book.title" class="fav-cover" @click="$router.push(`/books/${fav.book.id}`)" @error="e => e.target.src='https://picsum.photos/seed/default/200/300'" />
          <div class="fav-info">
            <router-link :to="`/books/${fav.book.id}`"><h3>{{ fav.book.title }}</h3></router-link>
            <p>{{ fav.book.author }}</p>
            <p class="fav-date">Favorited on {{ new Date(fav.created_at).toLocaleDateString() }}</p>
          </div>
          <el-button type="danger" plain @click="handleRemove(fav)">Remove</el-button>
        </div>
      </div>
    </template>
    <el-empty v-else description="No favorites yet" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getFavorites, removeFavorite } from '../api/endpoints'

const favorites = ref([])
const loading = ref(true)

async function fetchFavorites() {
  loading.value = true
  try {
    const res = await getFavorites()
    favorites.value = res.data.results || res.data
  } catch (e) {
    favorites.value = []
  }
  loading.value = false
}

async function handleRemove(fav) {
  try {
    await removeFavorite(fav.id)
    favorites.value = favorites.value.filter(f => f.id !== fav.id)
    ElMessage.success('Removed')
  } catch (e) {
    ElMessage.error('Failed to remove')
  }
}

onMounted(fetchFavorites)
</script>

<style scoped>
.favorites-page { max-width: 900px; margin: 0 auto; padding: 0 32px; }
h1 { margin-bottom: 36px; font-size: 28px; font-weight: 700; color: #1a1815; letter-spacing: -0.5px; }
.fav-list { display: flex; flex-direction: column; }
.fav-item {
  display: flex; align-items: center; gap: 24px;
  padding: 22px 0;
  border-bottom: 1px solid #f2ede7;
}
.fav-cover { width: 80px; height: 114px; object-fit: cover; border-radius: 8px; cursor: pointer; box-shadow: 0 1px 4px rgba(0,0,0,0.08); flex-shrink: 0; }
.fav-info { flex: 1; min-width: 0; }
.fav-info h3 { font-size: 16px; font-weight: 600; color: #1a1815; margin-bottom: 3px; }
.fav-info p { color: #a0988c; font-size: 13px; }
.fav-date { font-size: 12px; color: #b8b0a4; margin-top: 6px; }
</style>
