#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    utils.log_helper
    ~~~~~~~~~~~~~~~~

    write log to file and echo to stdout.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/kokkuri
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import os
import logging.handlers

t = os.path.dirname(os.path.abspath(__file__))
t = os.path.join(t, "../logs/kokkuri-agent.log")
log_filename = t

logger = logging.getLogger(__name__)

logger.setLevel("DEBUG")
file_handler = logging.handlers.TimedRotatingFileHandler(log_filename, when="midnight", backupCount=30)
file_formatter = logging.Formatter(
    fmt='[%(levelname)s] [%(threadName)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
