# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core.api import ThePirateBayApi
from core.models import Torrent
from core.serializers import TorrentSerializer

TPB = ThePirateBayApi()


class TorrentViewSet(ModelViewSet):
    queryset = Torrent.objects.all()
    serializer_class = TorrentSerializer


class SearchView(APIView):
    """
    View used to search series over ThePirateBayApi.
    E.g of search: /api/search?name={search phrase}
    """
    http_method_names = ['get']

    def get(self, request):
        if request.query_params.get('name', None) is None:
            # There must be a name to search for
            data = {"detail": "You need to pass something to search on querystring 'name'"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        result_list = TPB.search(self.request.query_params['name'])
        data = {
            'name': self.request.query_params['name'],
            'results': result_list
        }

        return Response(data, status=status.HTTP_200_OK)
