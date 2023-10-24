# -*- coding: utf-8 -*-
# @Author: Oleg Suvorinov
# @Date:   2023-10-19 18:36:55
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2023-10-19 18:37:03

import logging
import logging.config
import os

import yaml


def setup_logging(
    path='logging.yaml',
    default_level=logging.INFO
):
    """Setup logging configuration
        """

    create_trace_loglevel(logging)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def get(name):
    logger = logging.getLogger(name)
    return logger


def create_trace_loglevel(logging):
    """Add TRACE log level and Logger.trace() method.
    """

    logging.TRACE = 5
    logging.addLevelName(logging.TRACE, "TRACE")

    def _trace(logger, message, *args, **kwargs):
        if logger.isEnabledFor(logging.TRACE):
            logger._log(logging.TRACE, message, args, **kwargs)

    logging.Logger.trace = _trace
