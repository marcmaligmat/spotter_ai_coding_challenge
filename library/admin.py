from .models import BookShelf, Shelf, Favorite
from django.contrib import admin
from .models import Author, Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn',
                    'average_rating')
    search_fields = ('title', 'author__name', 'isbn', 'description')
    list_filter = ('language',)
    ordering = ('-id',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role')
    search_fields = ('id', 'name')
    list_filter = ('role',)
    ordering = ('name',)


@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ('book', 'shelf', 'count')
    search_fields = ('book__title', 'shelf__name')
    list_filter = ('shelf',)


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Favorite)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ('book', 'user')
