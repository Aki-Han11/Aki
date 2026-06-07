<template>
  <div class="book-grid-wrapper">
    <el-row :gutter="24">
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
/* Clean gallery grid — no card borders, image-forward */
.book-card {
  cursor: pointer; margin-bottom: 28px;
  transition: transform 0.3s ease;
}
.book-card:hover { transform: translateY(-4px); }
.book-card:hover .book-card-cover img { box-shadow: 0 8px 24px rgba(0,0,0,0.10); }

.book-card-cover { width: 100%; aspect-ratio: 2/3; overflow: hidden; border-radius: 10px; background: #f0f0f0; }
.book-card-cover img {
  width: 100%; height: 100%; object-fit: cover; display: block;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  transition: box-shadow 0.3s ease;
  border-radius: 10px;
}

.book-card-info { padding: 12px 4px 0; }
.book-title {
  font-size: 14px; font-weight: 600; color: #1c1917;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  margin: 0 0 4px; line-height: 1.3;
}
.book-author {
  font-size: 13px; color: #a0988c;
  margin-bottom: 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.book-bottom { display: flex; justify-content: space-between; align-items: center; }
.book-price { font-size: 15px; color: #1a1815; font-weight: 700; }
.book-tag { background: #f0f0f0 !important; color: #8b7e74 !important; border: none !important; font-size: 11px !important; }
.loading-box { padding: 40px; }
</style>
