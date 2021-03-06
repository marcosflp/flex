# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-23 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='torrent',
            name='themoviedb_url',
        ),
        migrations.AddField(
            model_name='torrent',
            name='themoviedb_movie_id',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='torrent',
            name='themoviedb_tvshow_id',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='torrent',
            name='type',
            field=models.CharField(choices=[(b'movie', b'Movie'), (b'tvshow', b'Tv Show'), (b'documentary', b'Documentary')], max_length=16),
        ),
    ]
