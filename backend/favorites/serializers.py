from rest_framework import serializers
from .models import Favorite
from books.serializers import BookListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'book', 'book_id', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('book',)
