# -*- coding: utf-8 -*-
# @Author: suvorinov
# @Date:   2023-10-07 16:12:30
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-10-29 10:16:56

import logging
import pprint
from typing import List, Dict

import requests
from bs4 import BeautifulSoup as BS

from py_random_useragent import UserAgent

logger = logging.getLogger(__name__)


class ScrapyProxy(object):
    """Class scrapers proxies from free-proxy-list.net"""

    def __init__(self):
        super(ScrapyProxy, self).__init__()
        self.url = 'https://free-proxy-list.net/'
        self.proxies = list()

    def __collect_proxy(self, contents: list) -> Dict:
        contents = contents.find_all('td')
        _proxy = {
            "host": "no",
            "port": "no",
            "country": "no",
            "anonymity": "no",
            "schema": "no"
        }
        if contents[0].contents:
            _proxy["host"] = contents[0].contents[0]
        if contents[1].contents:
            _proxy["port"] = contents[1].contents[0]
        if contents[2].contents:
            _proxy["country"] = contents[2].contents[0]
        if contents[3].contents:
            _proxy["anonymity"] = contents[4].contents[0]
        if contents[5].contents:
            _proxy["schema"] = contents[5].contents[0]

        return _proxy

    def scrapy_proxies(self) -> List:
        logger.info(f'Scraping proxies from {self.url}')
        try:
            headers = {
                'User-Agent': UserAgent().get_ua()
            }
            resp = requests.get(
                self.url,
                headers=headers,
                timeout=10
            )
        except requests.exceptions.RequestException as e:
            logger.error(f'Request to {self.url} failed: ', e)
            return self.proxies

        try:
            soup = BS(resp.text, 'html.parser').find('section', id='list')
            _trs = soup.find_all('tr')
            del _trs[0]
            for _tr in _trs:
                _proxy = self.__collect_proxy(_tr)
                if _proxy:
                    self.proxies.append(_proxy)
        except Exception:
            logger.error('Error during parse data', exc_info=True)
        finally:
            return self.proxies[:10]


if __name__ == '__main__':
    p = ScrapyProxy()
    p.scrapy_proxies()

    pprint.pprint(p.proxies[:3])
