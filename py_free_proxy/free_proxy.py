# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-10-18 18:46:53
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-10-29 10:36:43

import sys
import os
import logging
import time
from multiprocessing.dummy import Pool, current_process
# from gevent.pool import Pool
from importlib import import_module
from typing import List, Dict

import requests

from py_random_useragent import UserAgent

sys.setrecursionlimit(10000)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_object(path):
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError(
            "Module '%s' doesn't define any object named '%s'" % (module, name)
        )

    return obj


class FreeProxy(object):
    """Docstring for FreeProxy"""

    base_dir = os.path.dirname(__file__)

    def __init__(self) -> None:
        self.plugins = []
        self.scrapy_proxies = []
        self.alive_proxies = []

        self.country = 'US'
        self.schema = 'http'
        self.anonymity = True

        self.origin_ip = None

        self.__load_plugins()

    def __load_plugins(self) -> None:
        """Docstring for __load_plugins"""
        logger.info("Load plugins...")
        for plugin_name in os.listdir(os.path.join(self.base_dir, 'plugins')):
            if os.path.splitext(plugin_name)[1] != '.py' or \
                    plugin_name == '__init__.py':
                continue

            try:
                cls = load_object("py_free_proxy.plugins.%s.ScrapyProxy" %
                                  os.path.splitext(plugin_name)[0])
            except Exception as e:
                logger.error(
                    "Load Plugin %s error: %s" % (plugin_name, str(e))
                )
                continue

            inst = cls()
            # inst.proxies = copy.deepcopy(self.valid_proxies)
            self.plugins.append(inst)

    def __get_origin_ip(self) -> None:
        logger.info("Get origin ip...")
        rp = requests.get(
            'http://httpbin.org/get',
            headers={"User-Agent": UserAgent().get_ua()}
        )
        self.origin_ip = rp.json().get('origin', '')
        logger.info("Current Ip Address: %s" % self.origin_ip)

    def __check_proxy(self, proxy: dict, schema: str = 'http') -> Dict:
        _proxy = dict()

        return _proxy

    def __check_scrapy_proxies(self) -> None:
        logger.info("Check scrapy proxies")
        with Pool() as pool:
            for proxy in self.scrapy_proxies:
                result = pool.apply_async(self.__check_proxy, (proxy, 'http'))
            pool.close()
            pool.join()

    def __get_scrapy_proxies(self):
        if not self.plugins:
            logger.error("[x] No plugins found")
            self.scrapy_proxies = []
            return

        self.__get_origin_ip()

        logger.info("Get proxies...")
        with Pool() as pool:
            results = [pool.apply_async(plugin.scrapy_proxies, ()) for plugin in self.plugins] # noqa
            result = [x for p in results for x in p.get(timeout=2 * 60)]
            self.scrapy_proxies.extend(result)
            pool.close()
            pool.join()

        return

    def get_proxies(self,
                    country: str = 'US',
                    schema: str = 'http',
                    anonymity: bool = True,
                    amount: int = 10) -> List[Dict]:
        self.country = country
        self.schema = schema
        self.anonymity = anonymity

        self.__get_scrapy_proxies()
        self.__check_scrapy_proxies()

    def validate_proxy(self,
                       proxy: dict,
                       scheme: str = 'http'
                       ) -> Dict:
        host = proxy.get('host')
        port = proxy.get('port')

        request_proxies = {
            scheme: "%s:%s" % (host, port)
        }

        request_begin = time.time()
        _url = "%s://httpbin.org/get?show_env=1&cur=%s" % (
            scheme, request_begin)
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
