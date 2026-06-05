from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Rating
from books.models import Book


class RatingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        rating_value = request.data.get('rating', 5)
        if not book_id:
            return Response({'error': 'book_id required'}, status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.get(id=book_id)
        rating, created = Rating.objects.update_or_create(
            user=request.user, book=book,
            defaults={'rating': rating_value}
        )
        return Response({
            'id': rating.id,
            'book_id': book.id,
            'rating': rating.rating,
            'created_at': rating.created_at,
        })
