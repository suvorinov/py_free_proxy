# -*- coding: utf-8 -*-
# @Author: suvorinov
# @Date:   2023-10-07 10:22:22
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-10-09 17:10:31

import argparse


def main(args=None):
    parser = argparse.ArgumentParser(
        prog='free_proxy',
        description='Getting a "live" free proxy')  # noqa

    parser.add_argument(
        "-q", "--quiet",
        help="quiet mode (no console logs)",
        action="store_true")

    args = parser.parse_args()


if __name__ == '__main__':
    main()
