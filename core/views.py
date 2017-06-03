# -*- coding: utf-8 -*-
import libtorrent
import os
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api import ThePirateBayApi
from core.models import Torrent
from core.serializers import UserSerializer, SearchSerializer

TPB = ThePirateBayApi()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'username', 'first_name', 'email', 'is_staff', 'is_superuser')


@api_view()
def load_torrents(request):
    torrent_list = list()
    for torrent in Torrent.objects.all():
        torrent_list.append(torrent.name)
        torrent.save()

    return Response(torrent_list)


class TorrentView(APIView):
    http_method_names = ['get', 'post', 'put', 'delete']

    def get(self, request):
        """ Show the status of the Torrents_handler """
        state_list = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating',
                      '?']
        torrent_list = []

        for torrent in settings.TORRENTS_HANDLE_DICT.values():
            torrent_status = torrent.status()

            if torrent_status.has_metadata:
                t_title = torrent.get_torrent_info().name()
            else:
                t_title = "-----"

            torrent_list.append({'episode': t_title,
                                 'complete_percent': torrent_status.progress * 100,
                                 'download': torrent_status.download_rate / 1000,
                                 'up': torrent_status.upload_rate / 1000,
                                 'peers': torrent_status.num_peers,
                                 'state': state_list[torrent_status.state],
                                 'completed_time': torrent_status.completed_time,
                                 'paused': torrent_status.paused,
                                 'sequential_download': torrent_status.sequential_download})

        return Response(torrent_list)

    def post(self, request):
        """ Add torrents to the Torrents_Handler """
        torrent = Torrent.objects.create(name=request.data.get('name'),
                                         magnet_link=request.data.get('magnet_link'))
        if not torrent.pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request):
        """ Make changes on the Torrents_handler """
        pass

    def delete(self, request):
        """ Delete a torrent from the Torrents_handler """
        pass


class Result(object):
    def __init__(self, title, result):
        self.title = title
        self.result = result


class SearchView(APIView):
    """
    View used to search series over ThePirateBayApi.
    E.g of search general: /api/search?title
    """

    def get(self, request):
        # validate if has a title to search
        if not request.query_params.get('title'):
            return Response(status=status.HTTP_200_OK)

        if request.query_params.get('season'):
            result_list = self.get_season()
        else:
            result_list = self.get_general()

        result = Result(request.query_params.get('title'), result_list)
        serializer = SearchSerializer(result)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_season(self):
        try:
            season = int(self.request.query_params.get('season'))
        except ValueError:
            raise ValueError('No valid season was specified on the search.')

        return TPB.search_serie_season(self.request.query_params.get('title'), season=season)

    def get_general(self):
        return TPB.search(self.request.query_params.get('title'))


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def __init__(self):
        super(HomeView, self).__init__()
        self.pb = ThePirateBayApi()

        # def dispatch_request(self):
        #     pass
        #
        # def search(self):
        #     """ Search for torrents with ThePirateBay API """
        #     context = {'search_result_list': [],
        #                'search_result_list_message': None,
        #                'session_torrent_list': [],
        #                'session_torrent_list_message': None,
        #                'is_season_search': False}
        #
        #     if request.args.get('search_type') == 'general':
        #         result_list, message = self.search_general()
        #
        #         context['search_result_list'].extend(result_list)
        #         if message:
        #             context['search_result_list_message'] = message
        #
        #     elif request.args.get('search_type') == 'season':
        #         result_list, message = self.search_season()
        #         context['search_result_list'].extend(result_list)
        #         context['is_season_search'] = True
        #
        #     return render_template('home', context=context)
        #
        # def search_general(self):
        #     message = ''
        #     result = self.pb.search(title=request.args.get('q'))
        #
        #     if not result:
        #         message = 'No results found with: %s' % request.args.get('q')
        #
        #     return result['result'], message
        #
        # def search_season(self):
        #     message = ''
        #
        #     re_season = re.search(r's([0-9]{1,2})$', self.pb.search(title=request.args.get('q')), re.IGNORECASE)
        #     if re_season:
        #         season = re_season.group(1)
        #     else:
        #         message = 'No season was specified on the search. E.g of a valid search: Prison Break s01'
        #         return [], message
        #
        #     result_list = self.pb.search_serie_season(request.args.get('q'), season=season)
        #     if not result_list:
        #         message = 'No results found with: %s' % request.args.get('q')
        #
        #     return result_list, message
        #
        # def add(self):
        #     """ Add a torrent to the SESSION"""
        #     SESSION.add_magnet_uri()
        #
        # def remove(self):
        #     """ Remove a torrent from SESSION """
        #
        # def get_torrents_on_session(self):
        #     """ Get all torrents on the SESSION """
        #     context = {'session_torrent_list': [],
        #                'session_torrent_list_message': None}
        #
        #     context['session_torrent_list'].extend(SESSION.status_of_torrents())
        #
        #     return render_template('home.html', context=context)

# class AddTorrent(MethodView):
#     def get(self):
#         # torrent = Torrent(session=LIBTORRENT_SESSION, magnet_link=request.args.get('magnet_link'))
#         # torrent.download()
#
#         return redirect(url_for('home'))
