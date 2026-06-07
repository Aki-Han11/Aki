from django.db import models
from users.models import User
from books.models import Book


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(default=5)  # 1-5 scale
    review = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} rated {self.book.title}: {self.rating}"
