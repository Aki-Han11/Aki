from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CartItem
from .serializers import CartItemSerializer, CartItemCreateSerializer
from books.models import Book
from orders.models import Order, OrderItem


def _has_purchased(user, book):
    """Check if a user has already purchased a book (paid or completed order)."""
    from orders.models import Order
    return Order.objects.filter(
        user=user,
        status__in=['paid', 'completed'],
        items__book=book
    ).exists()


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemCreateSerializer
        return CartItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.validated_data['book']
        quantity = serializer.validated_data.get('quantity', 1)

        if _has_purchased(request.user, book):
            return Response(
                {'error': 'You have already purchased this book.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, book=book,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return Response(
            CartItemSerializer(cart_item, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart_items = CartItem.objects.select_related('book').filter(user=request.user)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.book.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price, status='pending')

        for item in cart_items:
            OrderItem.objects.create(order=order, book=item.book, price=item.book.price)

        cart_items.delete()
        from .serializers import CartItemSerializer
        return Response({'order_id': order.id, 'total_price': str(total_price)}, status=status.HTTP_201_CREATED)
