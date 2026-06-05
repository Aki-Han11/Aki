<template>
  <div class="book-grid">
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
              <el-tag v-if="book.category_name" size="small" type="info">{{ book.category_name }}</el-tag>
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
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-bottom: 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}
.book-card-cover {
  width: 100%;
  aspect-ratio: 2/3;
  overflow: hidden;
  background: #f0f0f0;
}
.book-card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.book-card-info {
  padding: 12px;
}
.book-title {
  font-size: 14px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 4px;
}
.book-author {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.book-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.book-price {
  font-size: 16px;
  color: #f56c6c;
  font-weight: 700;
}
.loading-box {
  padding: 40px;
}
</style>
