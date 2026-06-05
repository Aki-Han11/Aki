from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.AdminUserViewSet, basename='admin-users')
router.register(r'books', views.AdminBookViewSet, basename='admin-books')
router.register(r'categories', views.AdminCategoryViewSet, basename='admin-categories')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', views.AdminStatsView.as_view(), name='admin-stats'),
    path('train-recommendations/', views.TrainRecommendationsView.as_view(), name='train-recommendations'),
]
