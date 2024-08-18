from typing import List
import json
from django.core.management.base import BaseCommand
from library.models import Book, Shelf, BookShelf, Author


def parse_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def parse_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


class Command(BaseCommand):
    help = 'Import book data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)
        parser.add_argument('--limit', type=int, default=None)
        parser.add_argument('--start', type=int, default=1,
                            help='Line number to start processing')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        limit = kwargs.get('limit', None)
        start = kwargs.get('start', 1)

        with open(json_file, 'r') as file:
            line_count = 1
            for line_number, line in enumerate(file, start=1):

                # Skip lines before the start line
                if line_number < start:
                    continue

                if limit:
                    if line_count > limit:
                        break

                line_count += 1
                bookshelf_instances = []
                item = json.loads(line)

                dataset_api_id = item.get('id', '')
                authors = item.get('authors', [])
                author_instances: List[Author] = []

                print(item)
                for author_data in authors:
                    api_id = author_data.get('id')
                    author, created = Author.objects.get_or_create(
                        api_id=api_id,
                        defaults={
                            'name': author_data.get('name', ''),
                            'role': author_data.get('role', '')
                        }
                    )

                    author_instances.append(author)

                # Create or update book instance
                book, created = Book.objects.update_or_create(
                    dataset_api_id=dataset_api_id,
                    defaults={
                        'title': item.get('title', ''),
                        'author_name': item.get('author_name', ''),
                        'author_id': item.get('author_id', ''),
                        'work_id': item.get('work_id', ''),
                        'isbn': item.get('isbn', ''),
                        'isbn13': item.get('isbn13', ''),
                        'language': item.get('language', ''),
                        'average_rating': parse_float(item.get('average_rating', 0.0)),
                        'rating_dist': item.get('rating_dist', ''),
                        'ratings_count': parse_int(item.get('ratings_count', 0)),
                        'text_reviews_count': parse_int(item.get('text_reviews_count', 0)),
                        'publication_date': item.get('publication_date', ''),
                        'original_publication_date': item.get('original_publication_date', ''),
                        'format': item.get('format', ''),
                        'edition_information': item.get('edition_information', ''),
                        'image_url': item.get('image_url', ''),
                        'publisher': item.get('publisher', ''),
                        'num_pages': parse_int(item.get('num_pages', 0)),
                        'series_id': item.get('series_id', ''),
                        'series_name': item.get('series_name', ''),
                        'series_position': item.get('series_position', ''),
                        'description': item.get('description', '')
                    }
                )
                if not created:
                    # If the book already exists, skip the rest of the loop
                    continue

                book.authors.set(author_instances)

                shelves = item.get('shelves', [])
                for shelf_data in shelves:
                    shelf_name = shelf_data.get('name')
                    shelf_count = shelf_data.get('count', 0)

                    shelf, _ = Shelf.objects.get_or_create(
                        name=shelf_name)

                    bookshelf_instances.append(
                        BookShelf(
                            book=book,
                            shelf=shelf,
                            count=shelf_count
                        )
                    )

                # Bulk create BookShelf instances
                if bookshelf_instances:
                    BookShelf.objects.bulk_create(
                        bookshelf_instances)

        self.stdout.write(self.style.SUCCESS(
            'Successfully imported book data'))
