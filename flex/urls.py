"""flex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework import routers

from core.views import UserViewSet, SearchView, TorrentView, load_torrents

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/api/', permanent=False), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls), name='api'),
    url(r'^api/search', SearchView.as_view(), name='search'),
    url(r'^api/torrents', TorrentView.as_view(), name='torrent'),
    url(r'^api/load-torrents', load_torrents, name='torrent')
]
