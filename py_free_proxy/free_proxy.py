# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-10-18 18:46:53
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-10-24 19:03:16

import os
import logging
from importlib import import_module
from typing import List, Dict

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

    def __init__(
            self,
            country: str = 'US',
            schema: str = 'http',
            anonymity: bool = True) -> None:
        self.plugins = []

        self.country = country
        self.schema = schema
        self.anonymity = anonymity

        self.__load_plugins()

    def __load_plugins(self):
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

    def _get_proxies(self):
        logger.info("Get proxies...")
        for plugin in self.plugins:
            plugin.scrapy_proxies()


    def proxy_list(self) -> List[Dict]:
        return []

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


if __name__ == '__main__':
    p = FreeProxy()
    print(p.proxy_list())
    print(p.plugins)
