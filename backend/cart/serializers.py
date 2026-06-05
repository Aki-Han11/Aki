from rest_framework import serializers
from .models import CartItem
from books.serializers import BookListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'user', 'book', 'book_id', 'quantity', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('book', 'quantity')
