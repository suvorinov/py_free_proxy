# -*- coding: utf-8 -*-
# @Author: suvorinov
# @Date:   2023-10-07 10:22:22
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-10-30 12:38:31

import argparse
import logging
import pkg_resources

from py_free_proxy.free_proxy import FreeProxy


def main(args=None):

    _prog = "%(prog)s"
    _version = pkg_resources.get_distribution('py_free_proxy').version
    _prog_version = f"{_prog} {_version}"

    parser = argparse.ArgumentParser(
        prog='free_proxy',
        description='Getting a "live" free proxy')  # noqa

    parser.add_argument(
        "-q", "--quiet",
        help="quiet mode (no console logs)",
        action="store_true")

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=_prog_version
    )

    args = parser.parse_args()
    if args.quiet:
        # Disable console logging
        logging.getLogger().removeHandler(logging.getLogger().handlers[0])

    p = FreeProxy()
    proxies = p.get_proxies()
    print(p.scrapy_proxies)
