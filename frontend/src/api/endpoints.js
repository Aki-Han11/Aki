import api from './index'

// Auth
export const register = (data) => api.post('/register/', data)
export const login = (data) => api.post('/login/', data)
export const getProfile = () => api.get('/profile/')
export const updateProfile = (data) => api.put('/profile/', data)
export const changePassword = (data) => api.put('/change-password/', data)

// Books
export const getBooks = (params) => api.get('/books/', { params })
export const getBookDetail = (id) => api.get(`/books/${id}/`)
export const getHotBooks = (period = 'all') => api.get(`/books/hot/?period=${period}`)
export const getNewBooks = () => api.get('/books/new/')
export const getRecommendBooks = () => api.get('/books/recommend/')
export const getBookDownload = (id) => api.get(`/books/${id}/download/`)
export const searchBooks = (q) => api.get('/search/', { params: { q } })

// Categories
export const getCategories = () => api.get('/categories/')

// Favorites
export const getFavorites = () => api.get('/favorites/')
export const addFavorite = (bookId) => api.post('/favorites/', { book: bookId })
export const removeFavorite = (id) => api.delete(`/favorites/${id}/`)

// Cart
export const getCart = () => api.get('/cart/')
export const addToCart = (bookId) => api.post('/cart/', { book: bookId })
export const removeFromCart = (id) => api.delete(`/cart/${id}/`)
export const checkout = () => api.post('/cart/checkout/')

// Orders
export const getOrders = () => api.get('/orders/')
export const getOrderDetail = (id) => api.get(`/orders/${id}/`)
export const createOrder = (bookId) => api.post('/orders/', { book_id: bookId })
export const payOrder = (id) => api.put(`/orders/${id}/pay/`)
export const cancelOrder = (id) => api.put(`/orders/${id}/cancel/`)

// Downloads
export const getDownloads = () => api.get('/downloads/')

// Ratings
export const rateBook = (bookId, rating, review = '') => api.post('/ratings/', { book_id: bookId, rating, review })
export const getBookReviews = (bookId) => api.get(`/books/${bookId}/reviews/`)

// Admin
export const adminGetUsers = (params) => api.get('/admin/users/', { params })
export const adminUpdateUser = (id, data) => api.put(`/admin/users/${id}/`, data)
export const adminToggleUserActive = (id) => api.put(`/admin/users/${id}/toggle_active/`)
export const adminDeleteUser = (id) => api.delete(`/admin/users/${id}/`)

export const adminGetBooks = (params) => api.get('/admin/books/', { params })
export const adminCreateBook = (data) => api.post('/admin/books/', data)
export const adminUpdateBook = (id, data) => api.put(`/admin/books/${id}/`, data)
export const adminDeleteBook = (id) => api.delete(`/admin/books/${id}/`)

export const adminGetCategories = () => api.get('/admin/categories/')
export const adminCreateCategory = (data) => api.post('/admin/categories/', data)
export const adminUpdateCategory = (id, data) => api.put(`/admin/categories/${id}/`, data)
export const adminDeleteCategory = (id) => api.delete(`/admin/categories/${id}/`)

export const adminGetStats = () => api.get('/admin/stats/')
export const adminTrainRecommendations = () => api.post('/admin/train-recommendations/')

export const adminGetReviews = (params) => api.get('/admin/reviews/', { params })
export const adminDeleteReview = (id) => api.delete(`/admin/reviews/${id}/`)
