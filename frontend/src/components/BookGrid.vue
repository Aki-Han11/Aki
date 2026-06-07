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
/* ══════════════════════════════════════════════════════════════
   BookGrid — Refined Card Design
   Matches HomePage design language
   ══════════════════════════════════════════════════════════════ */

.book-card {
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 18px;
  overflow: hidden;
  cursor: pointer;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.025), 0 1px 2px rgba(0,0,0,0.03);
  transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.book-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 36px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
  border-color: #e2e8f0;
}

.book-card-cover {
  width: 100%;
  aspect-ratio: 2/3;
  overflow: hidden;
  background: #f8fafc;
}
.book-card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.book-card-info { padding: 18px 16px; }

.book-title {
  font-size: 14px; font-weight: 600; color: #1e293b;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  margin: 0 0 6px; line-height: 1.3;
}
.book-author {
  font-size: 13px; color: #94a3b8;
  margin-bottom: 10px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.book-bottom {
  display: flex; justify-content: space-between; align-items: center;
}
.book-price {
  font-size: 16px; color: #0f172a; font-weight: 700;
}
.book-tag {
  background: #f1f5f9 !important;
  border: 1px solid #e2e8f0 !important;
  color: #64748b !important;
}

.loading-box { padding: 40px; }
</style>
