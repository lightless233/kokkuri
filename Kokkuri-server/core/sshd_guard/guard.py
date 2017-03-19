#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    core.sshd_guard.guard
    ~~~~~~~~~~~~~~~~~~~~~

    Watch SSHD's event and make honeypots.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/kokkuri
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import time
import queue
import datetime

from models import Session, KokkuriSSHEvent
from utils import logger
from utils.docker_pot import DockerPot


class SSHDGuard(object):

    def __init__(self):
        super(SSHDGuard, self).__init__()

        self._exit_flag = False

        self.evil_task_queue = queue.Queue()

    def __guard_thread(self):

        logger.info("SSHD Guard start.")

        session = Session()
        while not self._exit_flag:

            # 拿出刚刚1分钟内的登录失败记录
            current_time = datetime.datetime.now()
            last_time = datetime.datetime.now() - datetime.timedelta(minutes=1)
            ssh_event_qs = session.query(KokkuriSSHEvent).filter(
                KokkuriSSHEvent.is_deleted != 0, KokkuriSSHEvent.created_time < current_time,
                KokkuriSSHEvent.created_time > last_time, KokkuriSSHEvent.result == 0
            ).all()

            analyze_dict = dict()

            # 计算每个来源IP失败的次数
            for qs in ssh_event_qs:
                source_ip = qs.source_ip
                if source_ip not in analyze_dict.keys():
                    analyze_dict[source_ip] = 0

                analyze_dict[source_ip] += 1

            # 将失败3次以上的IP扔到队列中，等待蜜罐线程处理
            evil_ip = list()
            for ip, fail_count in analyze_dict.items():
                if fail_count >= 3:
                    evil_ip.append(ip)
            self.evil_task_queue.put(evil_ip)
            time.sleep(10)

    def __make_pots_thread(self):
        session = Session()
        dp = DockerPot()
        dp.create_container()





