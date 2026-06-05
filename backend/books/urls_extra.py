from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
    path('', include(router.urls)),
]
