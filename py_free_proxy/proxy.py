# -*- coding: utf-8 -*-
# @Author: suvorinov
# @Date:   2023-10-16 14:55:28
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-10-17 20:37:52

import logging
from abc import ABC, abstractmethod
from typing import List, Dict
import time

import requests

from py_random_useragent import UserAgent
from .http_session import http_session

class Proxy(ABC):
    """docstring for Proxy"""
    def __init__(self):
        super(Proxy, self).__init__()
        self.http = http_session()
        self.proxies = []

    def validate_proxy(self, proxy: dict, scheme: str='http') -> Dict:
        host = proxy.get('host')
        port = proxy.get('port')

        request_proxies = {
            scheme: "%s:%s" % (host, port)
        }

        request_begin = time.time()
        _url = "%s://httpbin.org/get?show_env=1&cur=%s" % (scheme, request_begin)
        print(request_proxies)
        try:
            res = requests.get(
                _url,
                proxies=request_proxies,
                headers={"User-Agent": UserAgent().get_ua()},
                timeout=5
            ).json()
            print(res)
        except Exception as e:
            return None

        request_end = time.time()
        print(">>>> end")

        return {
            "type": scheme,
            "host": host,
            # "export_address": export_address,
            "port": port,
            # "anonymity": anonymity,
            # "country": country,
            "response_time": round(request_end - request_begin, 2),
            # "from": proxy.get('from')
        }

    @abstractmethod
    def get_proxies(self) -> List:
        return self.proxies
