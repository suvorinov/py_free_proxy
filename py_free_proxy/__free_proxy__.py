# -*- coding: utf-8 -*-
# @Author: suvorinov
# @Date:   2023-10-07 11:22:22
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-10-16 14:41:47

from multiprocessing import Pool, current_process


class FreeProxy(object):
    """docstring for FreeProxy"""

    def __init__(self, country: str='US', schema: str='https'):
        super(FreeProxy, self).__init__()

        self._pool = Pool()
        self._country = country
        self._schema = schema

    def _check_proxy(self, proxy, test):
        pass

    def _chek_proxy_list(self, proxies):
        _proxies = list()

        def cb(p):
            if p:
                _proxies.append(p)
                print("Ok !!!")

        def cb_error():
            print("Error !!!")

        for item in proxies:
            with Pool as pool:
                _result = pool.apply_async(
                    self._check_proxy, 
                    (item, 'http'),
                    cb,
                    cb_error)

                _result = pool.apply_async(
                    self._check_proxy, 
                    (item, 'https'),
                    cb,
                    cb_error)


    def proxy_list(self):
        pass

    def proxy(self):
        pl = self.proxy_list()
        pass