# -*- coding: utf-8 -*-
import os
import re

from django.db import models
from django.conf import settings

from core.signals import add_torrent, remove_torrent


class Torrent(models.Model):
    name = models.CharField(max_length=64)
    magnet_link = models.CharField(max_length=254)
    size = models.CharField(max_length=16, null=True, blank=True)
    save_path = models.CharField(max_length=254, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def __get_save_path(self):
        # Split the name into a list
        word_list = list()
        if len(self.name.split(' ')) > 2:
            word_list = self.name.split(' ')
        elif len(self.name.split('.')) > 2:
            word_list = self.name.split('.')
        else:
            # TODO: configure an alert email function
            word_list.append(self.name)

        # Check if exist an oldest cine path with at least 60% of equal words with the current name
        existing_cine_folder_list = os.listdir(settings.ROOT_DOWNLOAD_FOLDER)
        minimum = len(word_list) * 50 / 100
        existing_cine_folder = ''

        for folder in existing_cine_folder_list:
            total_words_founded = 0
            for word in word_list:
                if word.lower() in folder.lower():
                    total_words_founded += 1

            if total_words_founded >= minimum:
                existing_cine_folder = folder
                break

        # Create a new path_name
        name_list = list()
        if self.is_serie:
            for word in word_list:
                if re.search(r'S[0-9]{2}E[0-9]{2}', word, re.I):
                    if not existing_cine_folder:
                        existing_cine_folder = '.'.join(map(lambda _word: str(_word).lower(), name_list))

                    name_list.append(word)
                    break
                else:
                    name_list.append(word)
        else:
            name_list = word_list

        path_name = '.'.join(map(lambda _word: str(_word).lower(), name_list))

        return os.path.join(settings.ROOT_DOWNLOAD_FOLDER, existing_cine_folder, path_name)

    @property
    def is_serie(self):
        return True if re.search(r'S[0-9]{2}E[0-9]{2}', self.name, re.I) else False

    def save(self, **kwargs):
        self.save_path = self.__get_save_path()
        return super(Torrent, self).save(**kwargs)


models.signals.post_save.connect(add_torrent, sender=Torrent)
models.signals.post_delete.connect(remove_torrent, sender=Torrent)
