# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.utils.text import slugify


def generate_pathname(name, cine_type, index=0):
    """ Returns a valid path """
    if index > 0:
        path = os.path.join(settings.ROOT_DOWNLOAD_FOLDER,
                            cine_type,
                            '{}({})'.format(slugify(name), index))
    else:
        path = os.path.join(settings.ROOT_DOWNLOAD_FOLDER,
                            cine_type,
                            slugify(name))

    if not os.path.exists(path):
        return path
    else:
        return generate_pathname(name, cine_type, index+1)
