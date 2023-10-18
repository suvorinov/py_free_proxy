# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-06-21 14:02:08
# @Last Modified by:   suvorinov
# @Last Modified time: 2023-10-12 16:40:55

from urllib3 import util

import requests
from requests import adapters

from py_random_useragent import UserAgent

RETRIES = 5
BACKOFF_FACTOR = 20.0
STATUS_FORCELIST = (500, 502, 504)


def http_session(
        user_agent: str = "",
        proxy: str = "",
        headers: dict = None,
) -> requests.Session:
    _session = requests.Session()

    _retry = util.Retry(
        total=RETRIES,
        read=RETRIES,
        connect=RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=STATUS_FORCELIST,
    )

    _adapter = adapters.HTTPAdapter(max_retries=_retry)
    _session.mount("http://", _adapter)
    _session.mount("https://", _adapter)

    if user_agent:
        _session.headers.update({"User-Agent": user_agent})
    else:
        _session.headers.update({"User-Agent": UserAgent().get_ua()})

    if headers:
        _session.headers.update(headers)

    if proxy:
        _session.proxies.update(
            {
                'http': proxy,
                'https': proxy
            }
        )

    return _session
