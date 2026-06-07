from rest_framework import viewsets, permissions, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum

from users.models import User
from users.serializers import AdminUserSerializer
from books.models import Book, Category, BookStats
from books.serializers import BookAdminSerializer, CategorySerializer
from orders.models import Order, OrderItem
from ratings.models import Rating


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.role == 'admin':
            return Response({'error': 'Cannot delete admin user'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = False
        user.save()
        return Response({'message': 'User disabled'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response(AdminUserSerializer(user).data)


class AdminBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookAdminSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']


class AdminCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]


class AdminStatsView(generics.GenericAPIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        total_users = User.objects.filter(role='user').count()
        total_books = Book.objects.count()
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(status__in=['paid', 'completed']).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        total_downloads = BookStats.objects.aggregate(
            total=Sum('download_count')
        )['total'] or 0

        # Top selling books
        top_books = Book.objects.annotate(
            purchase_count=Count('stats__purchase_count')
        ).order_by('-stats__purchase_count')[:10]
        from books.serializers import BookListSerializer
        top_books_data = BookListSerializer(top_books, many=True).data

        return Response({
            'total_users': total_users,
            'total_books': total_books,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'total_downloads': total_downloads,
            'top_books': top_books_data,
        })


class TrainRecommendationsView(generics.GenericAPIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            from recommendations.train import train_model
            result = train_model()
            if 'error' in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = Rating.objects.select_related('user', 'book').all().order_by('-created_at')

    def get_queryset(self):
        qs = Rating.objects.select_related('user', 'book').all()
        book_id = self.request.query_params.get('book_id')
        if book_id:
            qs = qs.filter(book_id=book_id)
        return qs.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        data = [{
            'id': r.id,
            'user': r.user.username,
            'book_id': r.book.id,
            'book_title': r.book.title,
            'rating': r.rating,
            'review': r.review,
            'created_at': r.created_at,
        } for r in qs]
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        review.delete()
        return Response({'message': 'Review deleted'}, status=status.HTTP_200_OK)
