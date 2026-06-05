from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from pathlib import Path

VUE_INDEX = Path(__file__).resolve().parent.parent.parent / 'frontend' / 'dist' / 'index.html'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth & user
    path('api/', include('users.urls')),
    # Books & categories & search
    path('api/books/', include('books.urls')),
    path('api/', include('books.urls_extra')),
    # User features
    path('api/favorites/', include('favorites.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/ratings/', include('ratings.urls')),
    path('api/downloads/', include('downloads.urls')),
    # Admin
    path('api/admin/', include('admin_panel.urls')),
]

# Serve Vue SPA — only if built frontend exists
if VUE_INDEX.exists():
    urlpatterns.append(
        re_path(r'^(?!api/|admin/|static/).*$', TemplateView.as_view(template_name='index.html'))
    )
