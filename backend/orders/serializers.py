from rest_framework import serializers
from .models import Order, OrderItem
from books.serializers import BookListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'book', 'price', 'created_at')


class OrderListSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'total_price', 'status', 'items_count', 'created_at')

    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'total_price', 'status', 'items', 'created_at')


class OrderCreateSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=False)
