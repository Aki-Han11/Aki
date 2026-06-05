from rest_framework import serializers
from .models import DownloadHistory
from books.serializers import BookListSerializer


class DownloadHistorySerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)

    class Meta:
        model = DownloadHistory
        fields = ('id', 'book', 'created_at')
