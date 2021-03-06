#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Kokkuri Agent
    ~~~~~~~~~~~~~

    The Agent's Entry Point.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/kokkuri
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import queue


from config import mmap


def main():
    """
    简单的把demo跑起来
    :return:
    """
    mmap.policy_queue = queue.Queue()


if __name__ == '__main__':
    main()
