from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=300)
    description = models.TextField(blank=True, default='')
    cover_url = models.URLField(blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    tags = models.CharField(max_length=500, blank=True, default='')
    download_url = models.URLField(blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    publish_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BookStats(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='stats')
    view_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    purchase_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)
    hot_score = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Book stats'

    def __str__(self):
        return f"Stats: {self.book.title}"

    def calculate_hot_score(self):
        self.hot_score = (
            self.view_count * 1 +
            self.favorite_count * 3 +
            self.purchase_count * 5 +
            self.download_count * 2
        )
        self.save()
