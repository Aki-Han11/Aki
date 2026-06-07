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
h1 { margin-bottom: 28px; font-size: 28px; font-weight: 700; color: #1a1815; letter-spacing: -0.4px; }
.fav-list { display: flex; flex-direction: column; gap: 14px; }
.fav-item {
  display: flex; align-items: center; gap: 18px;
  background: #fffdfa; padding: 18px; border-radius: 16px;
  border: 1px solid #f0ece6;
  box-shadow: 0 1px 3px rgba(0,0,0,0.018), 0 1px 2px rgba(0,0,0,0.022);
  transition: all 0.25s ease;
}
.fav-item:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.04); border-color: #e0d8cc; }
.fav-cover { width: 65px; height: 92px; object-fit: cover; border-radius: 8px; cursor: pointer; }
.fav-info { flex: 1; }
.fav-info h3 { font-size: 16px; font-weight: 600; color: #1a1815; margin-bottom: 4px; }
.fav-info p { color: #a0988c; font-size: 14px; }
.fav-date { font-size: 12px; color: #b8b0a4; margin-top: 4px; }
</style>
