from rest_framework import viewsets, permissions, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum

from users.models import User
from users.serializers import AdminUserSerializer
from books.models import Book, Category, BookStats
from books.serializers import BookAdminSerializer, CategorySerializer
from orders.models import Order, OrderItem


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
