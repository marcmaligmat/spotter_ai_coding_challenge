# Generated by Django 5.1 on 2024-08-18 02:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='author',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='published_date',
        ),
        migrations.RemoveField(
            model_name='book',
            name='summary',
        ),
        migrations.AddField(
            model_name='author',
            name='role',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='author_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='author_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='average_rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='edition_information',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='format',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='isbn13',
            field=models.CharField(blank=True, max_length=17, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='num_pages',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='original_publication_date',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='publication_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='rating_dist',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='ratings_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='series_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='series_position',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='text_reviews_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='work_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='BookShelf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
                ('shelf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.shelf')),
            ],
        ),
    ]
