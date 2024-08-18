from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    api_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    ratings_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0)
    text_reviews_count = models.PositiveIntegerField(default=0)
    fans_count = models.PositiveIntegerField(default=0)
    works_count = models.PositiveIntegerField(default=0)
    work_ids = models.JSONField(blank=True, null=True)
    book_ids = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class Shelf(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    dataset_api_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    author_name = models.CharField(max_length=255, null=True, blank=True)
    author_id = models.CharField(max_length=255, null=True, blank=True)
    work_id = models.CharField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    isbn13 = models.CharField(max_length=17, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    rating_dist = models.CharField(max_length=255, null=True, blank=True)
    ratings_count = models.IntegerField(null=True, blank=True)
    text_reviews_count = models.IntegerField(null=True, blank=True)
    publication_date = models.CharField(max_length=50, null=True, blank=True)
    original_publication_date = models.CharField(
        max_length=255, null=True, blank=True)
    format = models.CharField(max_length=50, null=True, blank=True)
    edition_information = models.CharField(
        max_length=100, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    num_pages = models.IntegerField(null=True, blank=True)
    series_id = models.CharField(max_length=255, null=True, blank=True)
    series_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    series_position = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title


class BookShelf(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.book.title} on {self.shelf.name} ({self.count})"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
