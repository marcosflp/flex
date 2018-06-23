# -*- coding: utf-8 -*-
from rest_framework import serializers

from core import TorrentSession
from core.models import Torrent


class TorrentSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Torrent
        fields = '__all__'
        read_only_fields = ('path', 'status')

    def create(self, validated_data):
        return Torrent.create(**validated_data)

    @staticmethod
    def get_status(obj):
        """ Returns the status of each Torrent """
        if not hasattr(TorrentSession, 'pool'):
            # Does not have any torrent downloading
            return 'No torrent downloading'

        state_list = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating',
                      '?']

        torrent = TorrentSession.pool[obj.pk]
        torrent_status = torrent.status()

        if torrent_status.has_metadata:
            t_title = torrent.get_torrent_info().name()
        else:
            t_title = "-----"

        return {'episode': t_title,
                'complete_percent': torrent_status.progress * 100,
                'download': torrent_status.download_rate / 1000,
                'up': torrent_status.upload_rate / 1000,
                'peers': torrent_status.num_peers,
                'state': state_list[torrent_status.state],
                'completed_time': torrent_status.completed_time,
                'paused': torrent_status.paused,
                'sequential_download': torrent_status.sequential_download}
