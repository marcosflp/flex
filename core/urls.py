from django.conf.urls import url
from rest_framework import routers

from core.views import *

urlpatterns = [
    url(r'^search', SearchView.as_view(), name='search'),
]

router = routers.DefaultRouter()
router.register(r'torrent', TorrentViewSet)

urlpatterns += router.urls
