# -*- coding: utf-8 -*-
import requests
import time
import re
from lxml import html


ORDER_BY = {'seeders': '7',
            'leeches': '9'}

CATEGORIES = {'audio': '100',
              'video': '200',
              'applications': '300',
              'games': '400',
              'porn': '500',
              'other': '600'}


class ThePirateBayApi(object):
    """
    API that handle requests/responses from thepiratebay.org to get and search torrents results.
    The response from thepiratebay it's not parsed in json! This api has the job get all responses, scrape data from it
    and return this data parsed in json.
    """

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    thepiratebay_search_link = "https://thepiratebay.org/search/"
    order_by = ORDER_BY
    category = CATEGORIES

    def search(self, title, paginator_index=0):
        """ Return the result found on search the title param """

        query = "{0}/{1}/{2}/{3}/".format(title, str(paginator_index), self.order_by['seeders'], self.category['video'])
        url = self.thepiratebay_search_link + query

        response = self._get(url)
        result = self._get_and_parse_result_list(response)

        return result

    def search_serie_season(self, serie_name, season, paginator_index=0):
        """ Search the entire season of a TV Show """

        episodes_list = []
        episode = 1
        attempts = 2

        # FIXME: This is not to be done like that
        while episode <= 30:
            search_phrase = "{} S{:02d}E{:02d}".format(serie_name, int(season), episode)
            query = "{0}/{1}/{2}/{3}/".format(search_phrase,
                                              paginator_index,
                                              self.order_by['seeders'],
                                              self.category['video'])

            url = self.thepiratebay_search_link + query
            response = self.__conn_request('GET', url)
            results = self._get_and_parse_result_list(response)

            if not results:
                attempts -= 1
                episode += 1
                if attempts >= 0:
                    continue
                else:
                    break

            episodes_list.append(results[0])
            episode += 1

        return episodes_list

    def _get(self, url):
        return self.__conn_request('GET', url)

    @staticmethod
    def _get_and_parse_result_list(response):
        """ Extract the list of results from the response and return the a list of data parsed to json"""

        tree = html.fromstring(response.content)
        torrent_list = []

        # result not found
        if len(tree.xpath('//table[@id="searchResult"]/tr')) == 0:
            return torrent_list

        torrent_tree_list = tree.xpath('//table[@id="searchResult"]/tr')

        for item_tree in torrent_tree_list:
            data_tree = {
                'title': item_tree.xpath('.//td/div[@class="detName"]/a/text()'),
                'size': item_tree.xpath('./td[2]/font/text()'),
                'link': item_tree.xpath('./td[2]/a[1]/@href'),
                'seeds': item_tree.xpath('./td[3]/text()'),
                'leeches': item_tree.xpath('./td[3]/text()')
            }

            # Normalise data and make validations
            data = {'position': len(torrent_list) + 1}

            title = data_tree['title']
            if title:
                if isinstance(title[0], basestring):
                    data['title'] = data_tree['title'][0]

            text = data_tree['size']
            if text:
                if isinstance(text[0], basestring):
                    text = text[0].encode('ascii', 'ignore').decode('ascii').strip()
                    re_size = re.search(r'size ([\d\.]+)\s?(\w+)', text, re.I)
                    if re_size:
                        data['size'] = (float(re_size.group(1)), re_size.group(2).lower())

            link = data_tree['link']
            if link:
                data['link'] = data_tree['link'][0]

            seeds = data_tree['seeds']
            if seeds:
                if isinstance(seeds, basestring):
                    data['seeds'] = int(seeds[0])

            leeches = data_tree['leeches']
            if leeches:
                if isinstance(leeches, basestring):
                    data['leeches'] = int(leeches[0])

            torrent_list.append(data)

        return torrent_list

    def __conn_request(self, method, url):
        """ Make requests """

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
