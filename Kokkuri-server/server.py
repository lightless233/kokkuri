#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Kokkuri Server
    ~~~~~~~~~~~~~~

    The Server's Entry Point.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/kokkuri
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from utils.watch_log import WatchLogFile
from core.sshd_parser import SSHDParser
from core.sshd_guard.guard import SSHDGuard
from utils.docker_pot import DockerPot
from config import mmap


def main():
    """
    先简单的临时把代码跑起来
    :return:
    """

    mmap.docker_pot = DockerPot()
    mmap.sshd_parser = SSHDParser()
    mmap.sshd_guard = SSHDGuard()

    wlf = WatchLogFile(mmap.sshd_raw_log_queue)
    wlf.start()
    wlf.join()


if __name__ == '__main__':
    main()
