# -*- coding: utf-8 -*-
# @Author: suvorinov
# @Date:   2023-10-16 14:55:00
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-10-16 15:10:36

from os import listdir
from os.path import basename, dirname

__all__ = [basename(f)[:-3] for f in listdir(dirname(__file__))
           if f[-3:] == ".py" and not f.endswith("__init__.py")]
