from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Rating
from books.models import Book
from orders.models import Order


def _has_purchased(user, book):
    """Check if a user has purchased a book (paid or completed order)."""
    return Order.objects.filter(
        user=user,
        status__in=['paid', 'completed'],
        items__book=book
    ).exists()


class RatingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        book_id = self.request.query_params.get('book_id')
        qs = Rating.objects.select_related('user').all()
        if book_id:
            qs = qs.filter(book_id=book_id)
        return qs.order_by('-created_at')

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        rating_value = request.data.get('rating', 5)
        review_text = request.data.get('review', '')

        if not book_id:
            return Response({'error': 'book_id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        if not _has_purchased(request.user, book):
            return Response(
                {'error': 'You must purchase this book before rating.'},
                status=status.HTTP_403_FORBIDDEN
            )

        rating, created = Rating.objects.update_or_create(
            user=request.user, book=book,
            defaults={'rating': rating_value, 'review': review_text}
        )
        return Response({
            'id': rating.id,
            'book_id': book.id,
            'rating': rating.rating,
            'review': rating.review,
            'user': rating.user.username,
            'created_at': rating.created_at,
        })

    def destroy(self, request, *args, **kwargs):
        rating = self.get_object()
        # Allow owner or admin to delete
        if rating.user != request.user and request.user.role != 'admin':
            return Response(
                {'error': 'Not authorized to delete this review.'},
                status=status.HTTP_403_FORBIDDEN
            )
        rating.delete()
        return Response({'message': 'Review deleted'}, status=status.HTTP_200_OK)
