# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-10-19 07:31:10
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-10-19 07:32:38


class FreeProxyException(Exception):
    '''Exception class with message as a required parameter'''

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)
