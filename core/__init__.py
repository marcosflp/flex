# -*- coding: utf-8 -*-

import libtorrent
from django.conf import settings

default_app_config = 'core.apps.CoreConfig'


class Session(libtorrent.session):

    def __init__(self, **kwargs):
        super(Session, self).__init__(**kwargs)

        self.pool = {}
        self.listen_on(6881, 6891)
        self.download_root_path = settings.ROOT_DOWNLOAD_FOLDER

    def __unicode__(self):
        return "Session that handler torrents download"

    def add(self, torrent):
        """ Add torrents and starts downloading it """
        from core.models import Torrent
        assert isinstance(torrent, Torrent)

        params = {
            'save_path': torrent.path,
            'storage_mode': libtorrent.storage_mode_t.storage_mode_sparse
        }
        torrent_handler = libtorrent.add_magnet_uri(self, torrent.magnet_link, params)

        self.pool[torrent.pk] = torrent_handler

        return None

    def remove(self, torrent):
        """ Remove a torrent from the self.pool """
        from core.models import Torrent

        assert isinstance(torrent, Torrent)
        assert torrent.pk in self.pool.keys()

        del self.pool[torrent.pk]
        return None

    def load_torrents(self):
        from core.models import Torrent

        # Load Torrents
        torrents = Torrent.objects.all()
        for torrent in torrents:
            self.add(torrent)

TorrentSession = Session()
