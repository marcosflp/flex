from django.contrib import admin

# Register your models here.
from core.models import Torrent


class TorrentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Torrent, TorrentAdmin)
