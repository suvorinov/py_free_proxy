# -*- coding: utf-8 -*-
# @Author: suvorinov
# @Date:   2023-10-07 16:12:30
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-10-18 14:35:26

import pprint
from typing import List, Dict

from bs4 import BeautifulSoup as BS

from py_free_proxy.proxy import Proxy


class FreeProxyListNet(Proxy):
    """docstring for FreeProxyListNet"""

    def __init__(self):
        super(FreeProxyListNet, self).__init__()
        self.url = 'https://free-proxy-list.net'

    def __collect_proxy(self, contents: list) -> Dict:
        contents = contents.find_all('td')
        _proxy = dict()
        _proxy['host'] = contents[0].contents[0]
        _proxy['port'] = contents[1].contents[0]

        return _proxy

    def get_proxies(self) -> List:
        try:
            resp = self.http.get(self.url)
            soup = BS(resp.text, 'html.parser').find('section', id='list')
            _trs = soup.find_all('tr')
            del _trs[0]
            for _tr in _trs:
                # _proxy = super(FreeProxyListNet, self).validate_proxy(self.__collect_proxy(_tr)) # noqa
                _proxy = self.__collect_proxy(_tr)
                if _proxy:
                    self.proxies.append(_proxy)
        except Exception as e:
            raise e
        finally:
            self.http.close()


if __name__ == '__main__':
    p = FreeProxyListNet()
    p.get_proxies()

    pprint.pprint(p.proxies)
