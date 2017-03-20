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
import threading

from models import Session, KokkuriSSHEvent, KokkuriSSHPot
from config import server_config, mmap
from utils import logger


class SSHDGuard(object):

    def __init__(self):
        super(SSHDGuard, self).__init__()

        self._exit_flag = False

        self.evil_task_queue = queue.Queue()

        self.docker_pot = mmap.docker_pot

        self.make_pots_thread = threading.Thread(target=self.__make_pots_thread, name="MakePotsThread")
        self.make_pots_thread.start()

        self.guard_thread = threading.Thread(target=self.__guard_thread, name="SSHDGuardThread")
        self.guard_thread.start()

    def stop(self):
        self._exit_flag = True

    def __guard_thread(self):

        logger.info("SSHD Guard start.")

        session = Session()
        while not self._exit_flag:

            logger.debug("Checking...")

            # 拿出刚刚1分钟内的登录失败记录
            current_time = datetime.datetime.now()
            last_time = datetime.datetime.now() - datetime.timedelta(minutes=2)

            logger.debug("current_time")
            logger.debug(current_time)

            logger.debug("last_time")
            logger.debug(last_time)

            ssh_event_qs = session.query(KokkuriSSHEvent).filter(
                KokkuriSSHEvent.is_deleted == 0, KokkuriSSHEvent.created_time < current_time,
                KokkuriSSHEvent.created_time > last_time, KokkuriSSHEvent.result == 0
            ).all()
            session.commit()

            analyze_dict = dict()
            logger.debug("ssh event qs")
            logger.debug(ssh_event_qs)

            # 计算每个来源IP失败的次数
            for qs in ssh_event_qs:
                source_ip = qs.source_ip
                if source_ip not in analyze_dict.keys():
                    analyze_dict[source_ip] = 0

                analyze_dict[source_ip] += 1
            logger.debug(analyze_dict)
            # todo: 次数改为可配置
            # todo: 跳过本地回环
            # 将失败5次以上的IP扔到队列中，等待蜜罐线程处理
            evil_ip = list()
            for ip, fail_count in analyze_dict.items():
                if fail_count >= 5:
                    evil_ip.append(ip)

            if len(evil_ip) != 0:
                self.evil_task_queue.put(evil_ip)

            # 进入sleep状态
            time.sleep(5)

    def __make_pots_thread(self):

        db_session = Session()

        while not self._exit_flag:
            if self.evil_task_queue.empty():
                time.sleep(5)
            evil_ip = self.evil_task_queue.get()
            logger.info("Get An Evil IP: {0}".format(evil_ip))

            for ip in evil_ip:

                # 检查这个attacker ip是不是已经绑定了蜜罐了
                qs = db_session.query(KokkuriSSHPot).filter(KokkuriSSHPot.attacker_ip == ip).first()
                if qs:
                    continue

                container_name = "{0}_honeypot".format(ip.replace(".", "_"))
                container_id, ssh_port = self.docker_pot.create_container(container_name)

                qs = KokkuriSSHPot(
                    container_name=container_name, container_id=container_id,
                    pot_ip=server_config.HONEYPOT_IP, attacker_ip=ip, ssh_port=ssh_port, status=1
                )

                db_session.add(qs)
                db_session.commit()





