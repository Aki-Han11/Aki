from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count

from .models import Order, OrderItem
from .serializers import OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer
from books.models import Book, BookStats


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderDetailSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)\
            .annotate(items_count=Count('items'))\
            .order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """Create order for a single book (direct purchase)."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data.get('book_id')
        book = Book.objects.get(id=book_id)
        order = Order.objects.create(user=request.user, total_price=book.price, status='pending')
        OrderItem.objects.create(order=order, book=book, price=book.price)
        return Response(
            OrderDetailSerializer(order, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['put'])
    def pay(self, request, pk=None):
        order = self.get_object()
        if order.user != request.user:
            return Response({'error': 'Not your order'}, status=status.HTTP_403_FORBIDDEN)
        if order.status != 'pending':
            return Response({'error': 'Order is not in pending status'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'paid'
        order.save()
        # Update purchase stats (prefetch items with book to avoid N+1)
        for item in order.items.select_related('book').all():
            if item.book:
                stats, _ = BookStats.objects.get_or_create(book=item.book)
                stats.purchase_count += 1
                stats.calculate_hot_score()
        return Response(OrderDetailSerializer(order).data)

    @action(detail=True, methods=['put'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.user != request.user:
            return Response({'error': 'Not your order'}, status=status.HTTP_403_FORBIDDEN)
        if order.status not in ['pending']:
            return Response({'error': 'Cannot cancel this order'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'cancelled'
        order.save()
        return Response(OrderDetailSerializer(order).data)
