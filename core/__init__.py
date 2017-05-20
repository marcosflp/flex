# -*- coding: utf-8 -*-
import libtorrent
import os
import re
from django.conf import settings


class Session(libtorrent.session):
    # FIXME: Add _ or __ before the methods that are only used internally

    def __init__(self, download_root_path):
        super(Session, self).__init__()

        self.pool = {}
        self.listen_on(6881, 6891)
        self.download_root_path = download_root_path

    def __unicode__(self):
        return "Session that handler torrents download"

    def add_magnet_uri(self, torrent_title, uri=None, season_uri_list=None):
        """ Add torrents in the TorrentPool and starts downloading it """
        params = {
            'save_path': self.get_save_path(torrent_title),
            'storage_mode': libtorrent.storage_mode_t.storage_mode_sparse
        }

        if uri:
            torrent_handler = libtorrent.add_magnet_uri(self, uri, params)
            self.add_to_pool(torrent_handler)

        elif season_uri_list:
            for uri in season_uri_list:
                torrent_handler = libtorrent.add_magnet_uri(self, uri, params)
                self.add_to_pool(torrent_handler)

        return None

    def get_save_path(self, torrent_title):
        """ Return the absolute path to save this torrent """
        word_list = []

        if len(torrent_title.split(' ')) > 2:
            word_list = torrent_title.split(' ')
        elif len(torrent_title.split('.')) > 2:
            word_list = torrent_title.split('.')
        else:
            return os.path.join(settings.ROOT_DOWNLOAD_FOLDER, torrent_title)

        # Generate path_name
        name_list = []
        if self.is_serie(torrent_title):
            for word in word_list:
                if re.search(r'S[0-9]{2}E[0-9]{2}', word, re.I):
                    name_list.append(word)
                    break
                else:
                    name_list.append(word)
        else:
            name_list = word_list

        path_name = '.'.join(map(lambda _word: str(_word).lower(), name_list))

        return os.path.join(settings.ROOT_DOWNLOAD_FOLDER, path_name)

    @staticmethod
    def is_serie(torrent_title):
        """ Check if the title is from a tv serie show """
        if re.search(r'S[0-9]{2}E[0-9]{2}', torrent_title, re.I):
            return True
        else:
            return False

    def add_to_pool(self, torrent_handler):
        """ Add a torent_handler to the pool """
        self.pool[str(len(self.pool.keys())+1)] = torrent_handler

        return None

    def remove(self, index):
        """ Remove a torrent from the self.pool """
        if isinstance(index, int):
            index = str(index)

        torrent_removed = self.pool.pop(index)

        # reindex
        values = self.pool.values()
        self.pool = {}
        for x in range(len(values)):
            self.pool[str(x+1)] = values[x]

        return None

    def status_of_torrents(self):
        """ Return the state of all torrents on the session """
        state = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating', '?']
        t_list = []

        for t in self.pool.itervalues():
            t_status = t.status()

            if t_status.has_metadata:
                t_title = t.get_torrent_info().name()
            else:
                t_title = "-----"

            t_list.append([t_title,
                           t_status.progress * 100,
                           t_status.download_rate / 1000,
                           t_status.upload_rate / 1000,
                           t_status.num_peers,
                           state[t_status.state]])

        return t_list
