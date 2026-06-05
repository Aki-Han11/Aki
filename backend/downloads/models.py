from django.db import models
from users.models import User
from books.models import Book


class DownloadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='downloads')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Download histories'

    def __str__(self):
        return f"{self.user.username} downloaded {self.book.title}"
