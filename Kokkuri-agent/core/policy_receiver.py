#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    core.receiver
    ~~~~~~~~~~~~~

    Listen a port and receive policy from server.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/kokkuri
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import socket
import threading

from config import agent_config, mmap
from utils import logger


class PolicyReceiver(threading.Thread):

    def __init__(self):
        super(PolicyReceiver, self).__init__()
        self.listen_port = agent_config.AGENT_LISTEN_PORT
        self._server = None

    def run(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(("0.0.0.0", self.listen_port))
        self._server.listen(10)

        while True:
            client, client_info = self._server.accept()

            policy_line = client.recv(2048)
            policy_line = policy_line.strip()
            policy_line = policy_line.decode()

            # todo: 验证策略合法性
            logger.debug("Put a policy to queue. length: {0}".format(len(policy_line)))
            mmap.policy_queue.put(policy_line)


