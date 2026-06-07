from rest_framework import serializers
from .models import Book, Category, BookStats


class CategorySerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'book_count', 'created_at')
        read_only_fields = ('id', 'created_at')


class BookStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStats
        fields = ('view_count', 'favorite_count', 'purchase_count', 'download_count', 'hot_score')


class BookListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'cover_url', 'category', 'category_name',
                  'tags', 'price', 'publish_date', 'created_at')


class BookDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    stats = BookStatsSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'cover_url', 'category',
                  'category_name', 'tags', 'download_url', 'price', 'publish_date',
                  'stats', 'created_at')


class BookAdminSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
