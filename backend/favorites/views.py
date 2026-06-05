from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Favorite
from .serializers import FavoriteSerializer, FavoriteCreateSerializer
from books.models import Book, BookStats


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return FavoriteCreateSerializer
        return FavoriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.validated_data['book']
        fav, created = Favorite.objects.get_or_create(user=request.user, book=book)
        if created:
            stats, _ = BookStats.objects.get_or_create(book=book)
            stats.favorite_count += 1
            stats.calculate_hot_score()
        return Response(
            FavoriteSerializer(fav, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book = instance.book
        instance.delete()
        stats = BookStats.objects.filter(book=book).first()
        if stats and stats.favorite_count > 0:
            stats.favorite_count -= 1
            stats.calculate_hot_score()
        return Response(status=status.HTTP_204_NO_CONTENT)
