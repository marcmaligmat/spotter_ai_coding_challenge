# Generated by Django 5.1 on 2024-08-18 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_shelf_remove_author_bio_remove_book_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='dataset_api_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
