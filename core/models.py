# -*- coding: utf-8 -*-

from django.db import models

from core import TorrentSession
from core.utils import generate_pathname


class Torrent(models.Model):
    """
    Torrent model
    """
    TYPE_MOVIE = 'movie'
    TYPE_TVSHOW = 'tvshow'
    TYPE_DOCUMENTARY = 'documentary'
    TYPE_CHOICES = (
        (TYPE_MOVIE, 'Movie'),
        (TYPE_TVSHOW, 'Tv Show'),
        (TYPE_DOCUMENTARY, 'Documentary')
    )

    name = models.CharField(max_length=64, unique=True)
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)

    themoviedb_movie_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    themoviedb_tvshow_id = models.PositiveIntegerField(unique=True, null=True, blank=True)

    magnet_link = models.CharField(max_length=1024, unique=True)
    size = models.CharField(max_length=16, null=True, blank=True, default='', help_text='E.g: 100mb')
    path = models.CharField(max_length=254, unique=True, help_text='Path where the cine will be downloaded')

    def __unicode__(self):
        return '{}: {} {}'.format(self.pk, self.name, self.size)

    @classmethod
    def create(cls,
               name,
               type,
               magnet_link,
               size,
               themoviedb_tvshow_id,
               themoviedb_movie_id):
        """
        Create action

        :param name: (string) Name of the cine
        :param type: (string) define whether the cine is a serie, movie or documentary
        :param magnet_link: (string) link to download the torrent
        :param size: (string) size of the torrent

        :raises: ValidationError, AssertionError

        :return: Torrent instance
        """
        existing_types_list = [cine_type[0] for cine_type in Torrent.TYPE_CHOICES]
        assert type in existing_types_list

        path = generate_pathname(name, type)

        # create
        torrent = cls.objects.create(name=name,
                                     type=type,
                                     magnet_link=magnet_link,
                                     size=size,
                                     path=path,
                                     themoviedb_tvshow_id=themoviedb_tvshow_id,
                                     themoviedb_movie_id=themoviedb_movie_id)

        # add to be downloaded
        TorrentSession.add(torrent)

        return torrent

    def delete(self, using=None, keep_parents=False):
        TorrentSession.remove(self)
        super(Torrent, self).delete(using, keep_parents)
