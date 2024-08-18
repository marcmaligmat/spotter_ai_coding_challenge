from typing import List
from django.db.models import Count, Q, Value
from typing import List
from library.models import Book, Shelf, Favorite
from django.db.models.functions import Coalesce


def recommend_books(user, limit: int = 5) -> List[Book]:
    # Get all favorite books for the user
    favorite_books = Favorite.objects.filter(user=user).values('book')
    favorite_book_ids = [book['book'] for book in favorite_books]
    favorite_books_query = Book.objects.filter(id__in=favorite_book_ids)

    # Extract favorite authors, series_ids, and languages
    favorite_authors_id = favorite_books_query.values_list(
        'author_id', flat=True).distinct()
    favorite_series_ids = favorite_books_query.values_list(
        'series_id', flat=True).distinct()
    favorite_languages = favorite_books_query.values_list(
        'language', flat=True).distinct()

    # Popular shelves
    popular_shelves = (
        Shelf.objects.filter(
            bookshelf__book__in=favorite_book_ids
        )
        .annotate(count=Count('bookshelf'))
        .order_by('-count')
        .values_list('id', flat=True)
    )[:20]

    # Recommendations by author
    recommendations_by_author = Book.objects.filter(
        author_id__in=favorite_authors_id
    ).exclude(
        id__in=favorite_book_ids
    ).filter(
        language__in=favorite_languages
    ).order_by(
        '-average_rating',
        '-ratings_count'
    )[:1]  # Get 1 recommendation based on authors

    # Recommendations by series
    recommendations_by_series = Book.objects.filter(
        series_id__in=favorite_series_ids
    ).exclude(
        id__in=favorite_book_ids
    ).filter(
        language__in=favorite_languages
    ).order_by(
        '-average_rating',
        '-ratings_count'
    )[:1]  # Get 1 recommendation based on series

    recommendations_by_shelves = (
        Book.objects.filter(
            bookshelf__shelf__in=popular_shelves
        )
        .exclude(
            id__in=favorite_book_ids
        )
        .exclude(
            # Exclude books by favorite authors to discover new books
            author_id__in=favorite_authors_id
        )

        .filter(
            language__in=favorite_languages
        )
        .annotate(
            shelf_popularity=Coalesce(
                Count('bookshelf', filter=Q(
                    bookshelf__shelf__in=popular_shelves)),
                Value(0)
            )
        )
        .order_by('-shelf_popularity', '-average_rating', '-ratings_count')
    )[:20]

    # Filter to ensure unique authors
    seen_authors = set()
    unique_recommendations_by_shelves = []
    for book in recommendations_by_shelves:
        # Check if the author_id is already in seen_authors
        if book.author_id not in seen_authors:
            seen_authors.add(book.author_id)
            unique_recommendations_by_shelves.append(book)
        # Stop if we have reached the limit
        if len(unique_recommendations_by_shelves) >= limit:
            break

    # Combine recommendations ensuring unique results
    recommendations = list(recommendations_by_author) + \
        list(recommendations_by_series) + \
        list(unique_recommendations_by_shelves)

    # Ensure the number of recommendations does not exceed the limit
    recommendations = list(
        {book.id: book for book in recommendations}.values())[:limit]

    return recommendations
