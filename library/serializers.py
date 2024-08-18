from rest_framework import serializers
from .models import Author, Book, BookShelf, Favorite


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    shelves = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_shelves(self, obj):
        # Get the related BookShelf objects and find the one with the highest count
        shelves = BookShelf.objects.filter(book=obj).order_by('-count')[:20]
        if shelves is None:
            return None
        return [
            {
                "name": bookshelf.shelf.name,
                "count": bookshelf.count
            }
            for bookshelf in shelves
        ]

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)

        # Remove shelves from the default representation
        shelves = representation.pop('shelves', None)

        # Add shelves to the end of the representation
        if shelves is not None:
            representation['shelves'] = shelves

        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['user', 'book']
        # Optionally, you can set 'user' to read-only to always assign the current user
        read_only_fields = ['user']
