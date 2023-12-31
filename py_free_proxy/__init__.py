# -*- coding: utf-8 -*-
# @Author: suvorinov
# @Date:   2023-10-06 10:22:22
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-10-27 16:57:09

__author__ = 'Oleg Suvorinov'
__email__ = 'suvorinovoleg@yandex.ru'
__version__ = '0.1.0'

import os

from py_free_proxy.logging import setup_logging

log_config = os.path.dirname(os.path.abspath(__file__)) + '/logging.yaml'
setup_logging(path=log_config)
