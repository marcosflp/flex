import libtorrent
from django.conf import settings

SESSION_HANDLE = settings.SESSION_HANDLE
TORRENTS_HANDLE_DICT = settings.TORRENTS_HANDLE_DICT


def add_torrent(instance, **kwargs):
    """ Add a torrent to the SESSION_HANDLE class to be downloaded. """
    params = {'save_path': instance.save_path,
              'storage_mode': libtorrent.storage_mode_t.storage_mode_sparse}
    torrent = libtorrent.add_magnet_uri(SESSION_HANDLE, instance.magnet_link, params)

    TORRENTS_HANDLE_DICT[instance.pk] = torrent

    return None


def remove_torrent(instance, **kwargs):
    """ Remove a torrent from the SESSION_HANDLE """
    pass
