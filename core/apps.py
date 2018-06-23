from django.apps import AppConfig
from django.db import OperationalError

from core import TorrentSession


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Load all torrents
        try:
            TorrentSession.load_torrents()
        except OperationalError:
            # raises when there is not table created
            pass
