<template>
  <div class="book-grid-wrapper">
    <el-row :gutter="20">
      <el-col :xs="12" :sm="8" :md="6" :lg="4" v-for="book in books" :key="book.id">
        <div class="book-card" @click="$router.push(`/books/${book.id}`)">
          <div class="book-card-cover">
            <img :src="book.cover_url" :alt="book.title" @error="onImgError" />
          </div>
          <div class="book-card-info">
            <h3 class="book-title" :title="book.title">{{ book.title }}</h3>
            <p class="book-author">{{ book.author }}</p>
            <div class="book-bottom">
              <span class="book-price">${{ book.price }}</span>
              <el-tag v-if="book.category_name" size="small" class="book-tag">{{ book.category_name }}</el-tag>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
    <div v-if="loading" class="loading-box">
      <el-skeleton :rows="3" animated />
    </div>
    <el-empty v-if="!loading && books.length === 0" description="No books found" />
  </div>
</template>

<script setup>
defineProps({
  books: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

function onImgError(e) {
  e.target.src = 'https://picsum.photos/seed/default/200/300'
}
</script>

<style scoped>
.book-card {
  background: #fffdfa;
  border: 1px solid #f0ece6;
  border-radius: 18px;
  overflow: hidden;
  cursor: pointer;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.018), 0 1px 2px rgba(0,0,0,0.022);
  transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.book-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 40px rgba(0,0,0,0.06), 0 5px 14px rgba(0,0,0,0.03);
  border-color: #e0d8cc;
}

.book-card-cover { width: 100%; aspect-ratio: 2/3; overflow: hidden; background: #faf7f2; }
.book-card-cover img { width: 100%; height: 100%; object-fit: cover; display: block; }

.book-card-info { padding: 18px 16px; }
.book-title {
  font-size: 14px; font-weight: 600; color: #1e1b18;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  margin: 0 0 6px; line-height: 1.3;
}
.book-author {
  font-size: 13px; color: #a0988c;
  margin-bottom: 10px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.book-bottom { display: flex; justify-content: space-between; align-items: center; }
.book-price { font-size: 16px; color: #1a1815; font-weight: 700; }
.book-tag { background: #f5f0e8 !important; border: 1px solid #e8e0d4 !important; color: #8b7e74 !important; }
.loading-box { padding: 40px; }
</style>
