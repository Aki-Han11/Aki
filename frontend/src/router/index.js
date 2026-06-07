import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'Home', component: () => import('../views/HomePage.vue') },
      { path: 'books', name: 'BookList', component: () => import('../views/BookListPage.vue') },
      { path: 'books/:id', name: 'BookDetail', component: () => import('../views/BookDetailPage.vue') },
      { path: 'new', name: 'NewBooks', component: () => import('../views/FeaturedPage.vue'), props: { type: 'new' } },
      { path: 'hot', name: 'HotBooks', component: () => import('../views/FeaturedPage.vue'), props: { type: 'hot' } },
      { path: 'recommended', name: 'RecommendedBooks', component: () => import('../views/FeaturedPage.vue'), props: { type: 'recommended' }, meta: { auth: true } },
      { path: 'search', name: 'Search', component: () => import('../views/SearchPage.vue') },
      { path: 'login', name: 'Login', component: () => import('../views/LoginPage.vue'), meta: { guest: true } },
      { path: 'register', name: 'Register', component: () => import('../views/RegisterPage.vue'), meta: { guest: true } },
      { path: 'profile', name: 'Profile', component: () => import('../views/ProfilePage.vue'), meta: { auth: true } },
      { path: 'favorites', name: 'Favorites', component: () => import('../views/FavoritesPage.vue'), meta: { auth: true } },
      { path: 'cart', name: 'Cart', component: () => import('../views/CartPage.vue'), meta: { auth: true } },
      { path: 'orders', name: 'Orders', component: () => import('../views/OrdersPage.vue'), meta: { auth: true } },
      { path: 'orders/:id', name: 'OrderDetail', component: () => import('../views/OrderDetailPage.vue'), meta: { auth: true } },
      { path: 'downloads', name: 'Downloads', component: () => import('../views/DownloadsPage.vue'), meta: { auth: true } },
    ],
  },
  {
    path: '/admin',
    component: () => import('../layouts/AdminLayout.vue'),
    meta: { admin: true },
    children: [
      { path: '', name: 'AdminDashboard', component: () => import('../views/admin/DashboardPage.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('../views/admin/UsersPage.vue') },
      { path: 'books', name: 'AdminBooks', component: () => import('../views/admin/BooksPage.vue') },
      { path: 'categories', name: 'AdminCategories', component: () => import('../views/admin/CategoriesPage.vue') },
      { path: 'recommendations', name: 'AdminRecommendations', component: () => import('../views/admin/RecommendationsPage.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userStr = localStorage.getItem('user')
  let user = null
  try { user = JSON.parse(userStr) } catch (e) {}

  if (to.meta.auth && !token) {
    return next('/login')
  }
  if (to.meta.admin && (!token || user?.role !== 'admin')) {
    return next('/')
  }
  if (to.meta.guest && token) {
    return next('/')
  }
  next()
})

export default router
