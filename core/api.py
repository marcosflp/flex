# -*- coding: utf-8 -*-
import requests
import time
import re
import urlparse
from lxml import html


class ThePirateBayApi(object):
    """
    API that handle requests/responses from thepiratebay.org to get and search torrents results.
    The response from thepiratebay it's not parsed in json! This api has the job get all responses, scrape data from it
    and return this data parsed in json.
    """

    thepiratebay_api = "https://thepiratebay.org/"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    order_by = {'seeders': '7',
                'leeches': '9'}
    categories = {'audio': '100',
                  'video': '200',
                  'applications': '300',
                  'games': '400',
                  'porn': '500',
                  'other': '600'}

    def search(self, name, paginator_index=0):
        """
        Search on the piratebay

        :param name: name to search on the pirate bay
        :param paginator_index: starts on the first page
        :return: {
                    'name': (string),
                    'size': (string),
                    'link': (string),
                    'seeds': (string),
                    'leeches': (string)
                }
        """
        query = "/search/{name_to_search}/{page_index}/{order_by}/{category}/".format(
            name_to_search=name,
            page_index=str(paginator_index),
            order_by=self.order_by['seeders'],
            category=self.categories['video']
        )

        uri = urlparse.urljoin(self.thepiratebay_api, query)
        response = self.__get(uri)
        result_list = self.__parse_response(response)

        return result_list

    def search_serie_season(self, serie_name, season, paginator_index=0):
        """ Search for all episodes of a season of a TV Show """
        raise NotImplemented

    @staticmethod
    def __parse_response(response):
        """ Extract the list of results from the response and return the a list of data parsed to a dict"""

        tree = html.fromstring(response.content)
        torrent_list = []

        # Validate if has at least one result
        if len(tree.xpath('//table[@id="searchResult"]/tr')) == 0:
            return torrent_list

        torrent_tree_list = tree.xpath('//table[@id="searchResult"]/tr')
        for item_tree in torrent_tree_list:
            torrent_info = {
                'name': item_tree.xpath('.//td/div[@class="detName"]/a/text()'),
                'size': item_tree.xpath('./td[2]/font/text()'),
                'link': item_tree.xpath('./td[2]/a[1]/@href'),
                'seeds': item_tree.xpath('./td[3]/text()'),
                'leeches': item_tree.xpath('./td[3]/text()')
            }

            # Validates and normalize data

            valid_data = {'position': len(torrent_list) + 1}

            if torrent_info.get('name'):
                valid_data['name'] = torrent_info['name'][0]

            if torrent_info.get('size'):
                torrent_size = torrent_info['size'][0].encode('ascii', 'ignore').decode('ascii').strip()
                torrent_size_regex = re.search(r'size ([\d\.]+)\s?(\w+)', torrent_size, re.I)
                if torrent_size_regex:
                    valid_data['size'] = float(torrent_size_regex.group(1)), torrent_size_regex.group(2).lower()

            if torrent_info.get('link'):
                valid_data['link'] = torrent_info['link'][0]

            if torrent_info.get('seeds'):
                valid_data['seeds'] = int(torrent_info['seeds'][0])

            if torrent_info.get('leeches'):
                valid_data['leeches'] = int(torrent_info['leeches'][0])

            torrent_list.append(valid_data)

        return torrent_list

    def __get(self, url):
        """ Makes GET request """
        return self.__conn_request('GET', url)

    def __conn_request(self, method, url):
        """ Makes requests """
        try:
            response = requests.request(method, url, headers=self.headers)
        except requests.Timeout:
            # Retry once, it could be a momentary overloaded server?
            time.sleep(3)
            try:
                response = requests.request(method, url, headers=self.headers)
            except Exception as e:
                raise e
        return response
