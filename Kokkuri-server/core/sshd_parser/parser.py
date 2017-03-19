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
import datetime
import threading

from config import mmap
from utils import logger
from models import Session, KokkuriSSHEvent


class SSHDParser(object):

    def __init__(self):

        # 初始化接收队列
        self.raw_log_queue = mmap.sshd_raw_log_queue = queue.Queue()

        # 退出标志
        self._exit_flag = False

        # 开新线程不停的解析每行log
        self.parse_thread = threading.Thread(target=self.__parse, name="SSHDParserThread", daemon=True)
        self.parse_thread.start()

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
        logger.debug("SSHD Parser start!")
        while not self._exit_flag:

            # 队里为空的时候则跳过
            if self.raw_log_queue.empty():
                time.sleep(2)
                continue

            raw_log_line = self.raw_log_queue.get()

            # 转成unicode
            raw_log_line = raw_log_line.decode()

            log_head, log_message = raw_log_line.split(": ", maxsplit=1)

            log_head = log_head.strip()
            log_message = log_message.strip()

            # 提取时间
            log_head_array = log_head.split(" ")
            event_time = "{0} {1} {2} {3}".format(
                log_head_array[0], log_head_array[1], log_head_array[2], datetime.datetime.today().year
            )
            event_time = datetime.datetime.strptime(event_time, "%b %d %H:%M:%S %Y")

            # 主机名
            target_host_name = log_head_array[3]
            temp = log_message.split(" ")
            item_count = 1
            result = 0

            if log_message.startswith("Accepted password"):
                user = temp[3]
                source_ip = temp[5]
                result = 1

            elif log_message.startswith("Failed password"):
                user = temp[3]
                source_ip = temp[5]

            elif log_message.startswith("message repeated"):
                user = temp[8]
                source_ip = temp[10]
                item_count = 2
            else:
                continue

            session = Session()
            for i in range(item_count):
                qs = KokkuriSSHEvent(user=user, source_ip=source_ip, target_host=target_host_name, result=result)
                qs.created_time = event_time
                session.add(qs)
                session.commit()

    def stop(self):
        self._exit_flag = True
