# Generated by Django 5.0.6 on 2024-12-05 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'directors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Directorsdetails',
            fields=[
                ('director_id', models.AutoField(primary_key=True, serialize=False)),
                ('display_name', models.TextField()),
            ],
            options={
                'db_table': 'directorsdetails',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'genre',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genredetails',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('display_name', models.TextField()),
            ],
            options={
                'db_table': 'genredetails',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Moviecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'moviecast',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Moviecastdetails',
            fields=[
                ('celebrity_id', models.AutoField(primary_key=True, serialize=False)),
                ('display_name', models.TextField()),
            ],
            options={
                'db_table': 'moviecastdetails',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('movie_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('production_year', models.IntegerField(blank=True, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('certificate', models.TextField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('votes', models.IntegerField(blank=True, null=True)),
                ('photo_url', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'movies',
                'managed': False,
            },
        ),
    ]
