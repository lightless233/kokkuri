#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    core.sshd_parser
    ~~~~~~~~~~~~~~~~

    SSHD log's parser.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/kokkuri
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import queue
import time
import threading

from config import mmap


class SSHDParser(object):

    def __init__(self):

        # 初始化接收队列
        self.raw_log_queue = mmap.sshd_raw_log_queue = queue.Queue()

        # 开新线程不停的解析每行log
        self.parse_thread = threading.Thread(target=None, name=None, daemon=None)
        self.parse_thread.start()

        # 退出标志
        self._exit_flag = False

    def __parse(self):
        """
        b'Mar 16 21:06:00 devel sshd[66973]: Received SIGHUP; restarting.'
        b'Mar 16 21:06:00 devel sshd[66973]: Server listening on 0.0.0.0 port 22.'
        b'Mar 16 21:06:00 devel sshd[66973]: Server listening on :: port 22.'
        b'Mar 16 21:06:23 devel sshd[68323]: Accepted password for root from 192.168.198.1 port 5055 ssh2'
        b'Mar 16 22:18:51 devel sshd[68521]: Failed password for root from 127.0.0.1 port 34172 ssh2'
        b'Mar 16 22:18:59 devel sshd[68521]: message repeated 2 times: [ Failed password for root from 127.0.0.1 port 34172 ssh2]'
        b'Mar 16 22:18:59 devel sshd[68521]: Connection closed by 127.0.0.1 port 34172 [preauth]'
        :return:
        """

        while not self._exit_flag:

            # 队里为空的时候则跳过
            if self.raw_log_queue.empty():
                time.sleep(2)
                continue

            raw_log_line = self.raw_log_queue.get()

            # 转成unicode
            raw_log_line = raw_log_line.decode()

            log_head, log_message = raw_log_line.split(":")
            
            log_message = log_message.strip()
            if log_message.startswith("Accepted password"):
                pass
            elif log_message.startswith("Failed password"):
                pass
            elif log_message.startswith("message repeated"):
                pass



    def stop(self):
        self._exit_flag = True
