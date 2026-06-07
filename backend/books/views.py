from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, permissions, status, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book, Category, BookStats
from .serializers import (
    BookListSerializer, BookDetailSerializer, CategorySerializer, BookAdminSerializer
)


class BookViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'tags']

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookAdminSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = Book.objects.all().order_by('-created_at')
        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs

    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
        stats, _ = BookStats.objects.get_or_create(book=book)
        stats.view_count += 1
        stats.calculate_hot_score()
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def hot(self, request):
        period = request.query_params.get('period', 'all')
        qs = BookStats.objects.all()
        if period == 'day':
            qs = qs.filter(updated_at__gte=timezone.now() - timedelta(days=1))
        elif period == 'week':
            qs = qs.filter(updated_at__gte=timezone.now() - timedelta(days=7))
        qs = qs.order_by('-hot_score')[:20]
        book_ids = qs.values_list('book_id', flat=True)
        books = Book.objects.filter(id__in=list(book_ids))
        books_dict = {b.id: b for b in books}
        books_ordered = [books_dict[bid] for bid in book_ids if bid in books_dict]
        serializer = BookListSerializer(books_ordered, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def new(self, request):
        books = Book.objects.all().order_by('-created_at')[:20]
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recommend(self, request):
        if not request.user.is_authenticated:
            books = Book.objects.all().order_by('?')[:12]
            serializer = BookListSerializer(books, many=True)
            return Response(serializer.data)
        try:
            from recommendations.predict import get_recommendations
            rec_ids = get_recommendations(request.user.id, 12)
            if rec_ids:
                books = Book.objects.filter(id__in=rec_ids)
                books_dict = {b.id: b for b in books}
                books_ordered = [books_dict[bid] for bid in rec_ids if bid in books_dict]
                serializer = BookListSerializer(books_ordered, many=True)
                return Response(serializer.data)
        except Exception:
            pass
        books = Book.objects.all().order_by('?')[:12]
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        book = self.get_object()
        from ratings.models import Rating
        ratings = Rating.objects.filter(book=book).select_related('user').order_by('-created_at')
        data = [{
            'id': r.id,
            'user': r.user.username,
            'rating': r.rating,
            'review': r.review,
            'created_at': r.created_at,
        } for r in ratings]
        return Response(data)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({'error': 'Login required'}, status=status.HTTP_401_UNAUTHORIZED)
        book = self.get_object()
        from orders.models import OrderItem
        purchased = OrderItem.objects.filter(
            order__user=request.user,
            order__status__in=['paid', 'completed'],
            book=book
        ).exists()
        if not purchased:
            return Response({'error': 'You need to purchase this book first'}, status=status.HTTP_403_FORBIDDEN)
        from downloads.models import DownloadHistory
        DownloadHistory.objects.get_or_create(user=request.user, book=book)
        stats, _ = BookStats.objects.get_or_create(book=book)
        stats.download_count += 1
        stats.calculate_hot_score()
        return Response({'download_url': book.download_url})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class SearchView(generics.ListAPIView):
    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        q = self.request.query_params.get('q', '')
        if q:
            return Book.objects.filter(
                Q(title__icontains=q) | Q(author__icontains=q) | Q(tags__icontains=q)
            ).order_by('-created_at')
        return Book.objects.none()
